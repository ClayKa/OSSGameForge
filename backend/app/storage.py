"""
Storage management for OSSGameForge using MinIO

Provides functions for uploading, downloading, and managing files in MinIO
object storage with proper error handling and logging.
"""
import io
import logging
import os
from typing import Optional
from minio import Minio
from minio.error import S3Error

logger = logging.getLogger(__name__)

# Initialize MinIO client
minio_client = None

def get_minio_client() -> Minio:
    """
    Get or create MinIO client instance
    
    Returns:
        Configured MinIO client
    """
    global minio_client
    
    if minio_client is None:
        endpoint = os.getenv("MINIO_ENDPOINT", "localhost:9000")
        access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
        secure = os.getenv("MINIO_SECURE", "false").lower() == "true"
        
        minio_client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        
        logger.info(f"Initialized MinIO client for endpoint: {endpoint}")
    
    return minio_client


# Convenience reference
minio_client = get_minio_client()


def upload_file_to_storage(
    bucket_name: str,
    object_name: str,
    data: io.BytesIO,
    length: int,
    content_type: str = "application/octet-stream"
) -> bool:
    """
    Upload file to MinIO storage
    
    Args:
        bucket_name: Name of the bucket
        object_name: Name/path of the object in the bucket
        data: File data as BytesIO stream
        length: Size of the data in bytes
        content_type: MIME type of the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_minio_client()
        
        # Ensure bucket exists
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"Created bucket: {bucket_name}")
        
        # Upload the file
        client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
            length=length,
            content_type=content_type
        )
        
        logger.info(f"Uploaded {object_name} to {bucket_name}")
        return True
        
    except S3Error as e:
        logger.error(f"Failed to upload {object_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error uploading file: {e}")
        return False


def download_file_from_storage(
    bucket_name: str,
    object_name: str
) -> Optional[bytes]:
    """
    Download file from MinIO storage
    
    Args:
        bucket_name: Name of the bucket
        object_name: Name/path of the object in the bucket
        
    Returns:
        File data as bytes or None if failed
    """
    try:
        client = get_minio_client()
        
        # Get object
        response = client.get_object(bucket_name, object_name)
        data = response.read()
        response.close()
        response.release_conn()
        
        logger.info(f"Downloaded {object_name} from {bucket_name}")
        return data
        
    except S3Error as e:
        logger.error(f"Failed to download {object_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error downloading file: {e}")
        return None


def delete_file_from_storage(
    bucket_name: str,
    object_name: str
) -> bool:
    """
    Delete file from MinIO storage
    
    Args:
        bucket_name: Name of the bucket
        object_name: Name/path of the object to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        client = get_minio_client()
        client.remove_object(bucket_name, object_name)
        logger.info(f"Deleted {object_name} from {bucket_name}")
        return True
        
    except S3Error as e:
        logger.error(f"Failed to delete {object_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error deleting file: {e}")
        return False


def get_file_url(
    bucket_name: str,
    object_name: str,
    expires_in: int = 3600
) -> Optional[str]:
    """
    Generate presigned URL for file access
    
    Args:
        bucket_name: Name of the bucket
        object_name: Name/path of the object
        expires_in: URL expiration time in seconds (default: 1 hour)
        
    Returns:
        Presigned URL or None if failed
    """
    try:
        client = get_minio_client()
        url = client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=expires_in
        )
        return url
        
    except S3Error as e:
        logger.error(f"Failed to generate URL for {object_name}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error generating URL: {e}")
        return None


def list_objects(
    bucket_name: str,
    prefix: Optional[str] = None
) -> list:
    """
    List objects in a bucket with optional prefix filter
    
    Args:
        bucket_name: Name of the bucket
        prefix: Optional prefix to filter objects
        
    Returns:
        List of object names
    """
    try:
        client = get_minio_client()
        objects = client.list_objects(
            bucket_name=bucket_name,
            prefix=prefix,
            recursive=True
        )
        
        return [obj.object_name for obj in objects]
        
    except S3Error as e:
        logger.error(f"Failed to list objects: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error listing objects: {e}")
        return []


def check_storage_health() -> dict:
    """
    Check MinIO storage health
    
    Returns:
        Health status dictionary
    """
    try:
        client = get_minio_client()
        # Try to list buckets as a health check
        buckets = client.list_buckets()
        
        return {
            "status": "healthy",
            "buckets_count": len(buckets),
            "endpoint": os.getenv("MINIO_ENDPOINT", "localhost:9000")
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "endpoint": os.getenv("MINIO_ENDPOINT", "localhost:9000")
        }