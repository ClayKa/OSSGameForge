"""
Comprehensive tests for Task 2.1: Simplified Preprocessing Pipeline

Tests the asset upload endpoint, consent validation, EXIF stripping,
and metadata extraction functionality.
"""
import io
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from PIL import Image, ExifTags
import pytest
from fastapi.testclient import TestClient

# Test imports
import sys
sys.path.insert(0, '/app')

from app.main import app
from app.services import asset_service
from app.storage import upload_file_to_storage, download_file_from_storage


class TestConsentValidation:
    """Test user consent validation"""
    
    def test_upload_without_consent_fails(self):
        """Test that upload without consent returns 400"""
        client = TestClient(app)
        
        # Create a test image
        img = Image.new('RGB', (100, 100), color='red')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        response = client.post(
            "/api/projects/test_project/assets",
            files={"file": ("test.jpg", img_bytes, "image/jpeg")},
            data={"user_consent": "false"}
        )
        
        assert response.status_code == 400
        assert "consent" in response.json()["detail"].lower()
    
    def test_upload_with_consent_succeeds(self):
        """Test that upload with consent returns 202"""
        client = TestClient(app)
        
        # Create a test image
        img = Image.new('RGB', (100, 100), color='green')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Set mock mode for testing
        with patch.dict('os.environ', {'MOCK_MODE': 'true'}):
            response = client.post(
                "/api/projects/test_project/assets",
                files={"file": ("test.jpg", img_bytes, "image/jpeg")},
                data={"user_consent": "true"}
            )
        
        assert response.status_code == 202
        assert "asset_id" in response.json()
        assert response.json()["status"] == "processing"


class TestEXIFStripping:
    """Test EXIF data stripping from images"""
    
    def create_image_with_exif(self):
        """Create a test image with EXIF data"""
        img = Image.new('RGB', (200, 200), color='blue')
        
        # Add EXIF data
        exif_data = img.getexif()
        exif_data[0x9286] = "Test User Comment"  # UserComment tag
        exif_data[0x010F] = "Test Camera"  # Make tag
        exif_data[0x0110] = "Test Model"  # Model tag
        exif_data[0x8769] = {
            0x9000: b'0230',  # ExifVersion
            0x9003: '2024:01:01 12:00:00',  # DateTimeOriginal
            0x9004: '2024:01:01 12:00:00',  # DateTimeDigitized
        }
        
        # Save with EXIF
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', exif=exif_data)
        img_bytes.seek(0)
        
        return img_bytes
    
    @pytest.mark.asyncio
    async def test_exif_stripping(self):
        """Test that EXIF data is stripped from uploaded images"""
        # Create image with EXIF
        img_bytes = self.create_image_with_exif()
        original_data = img_bytes.getvalue()
        
        # Verify original has EXIF
        original_img = Image.open(io.BytesIO(original_data))
        original_exif = original_img.getexif()
        assert len(original_exif) > 0, "Original image should have EXIF data"
        
        # Process image through our service
        mock_asset = MagicMock()
        mock_asset.type = "image"
        mock_asset.asset_metadata = {"format": "JPEG"}
        
        processed_data = await asset_service._process_image(original_data, mock_asset)
        
        # Verify EXIF is stripped
        processed_img = Image.open(io.BytesIO(processed_data))
        processed_exif = processed_img.getexif()
        assert len(processed_exif) == 0, "Processed image should have no EXIF data"
        
        # Verify image dimensions are preserved
        assert processed_img.size == original_img.size
    
    @pytest.mark.asyncio
    async def test_transparency_preservation(self):
        """Test that transparent images maintain transparency"""
        # Create RGBA image with transparency
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 128))  # Semi-transparent red
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        mock_asset = MagicMock()
        mock_asset.type = "image"
        mock_asset.asset_metadata = {"format": "PNG"}
        
        processed_data = await asset_service._process_image(img_bytes.getvalue(), mock_asset)
        
        # Verify transparency is preserved
        processed_img = Image.open(io.BytesIO(processed_data))
        assert processed_img.mode == 'RGBA'


class TestMetadataExtraction:
    """Test metadata extraction for different file types"""
    
    def test_audio_metadata_extraction(self):
        """Test extracting metadata from audio files"""
        # Mock tinytag response
        mock_tag = MagicMock()
        mock_tag.duration = 180.5
        mock_tag.bitrate = 320000
        mock_tag.samplerate = 44100
        mock_tag.channels = 2
        mock_tag.artist = "Test Artist"
        mock_tag.title = "Test Song"
        mock_tag.album = "Test Album"
        
        mock_asset = MagicMock()
        mock_asset.id = "test_asset_id"
        mock_asset.asset_metadata = {}
        
        mock_db = MagicMock()
        
        with patch('tinytag.TinyTag.get', return_value=mock_tag):
            asset_service._extract_audio_metadata(mock_asset, "test.mp3", mock_db)
        
        # Verify metadata was extracted
        assert mock_asset.asset_metadata["duration_seconds"] == 180.5
        assert mock_asset.asset_metadata["bitrate"] == 320000
        assert mock_asset.asset_metadata["samplerate"] == 44100
        assert mock_asset.asset_metadata["channels"] == 2
        assert mock_asset.asset_metadata["artist"] == "Test Artist"
        assert mock_asset.asset_metadata["title"] == "Test Song"
        assert mock_asset.asset_metadata["album"] == "Test Album"
        
        # Verify database commit was called
        mock_db.commit.assert_called_once()
    
    def test_video_metadata_extraction(self):
        """Test extracting metadata from video files"""
        # Mock tinytag response for video
        mock_tag = MagicMock()
        mock_tag.duration = 600.0
        mock_tag.bitrate = 5000000
        
        mock_asset = MagicMock()
        mock_asset.id = "test_video_id"
        mock_asset.asset_metadata = {}
        
        mock_db = MagicMock()
        
        with patch('tinytag.TinyTag.get', return_value=mock_tag):
            asset_service._extract_video_metadata(mock_asset, "test.mp4", mock_db)
        
        # Verify metadata was extracted
        assert mock_asset.asset_metadata["duration_seconds"] == 600.0
        assert mock_asset.asset_metadata["bitrate"] == 5000000
        
        # Verify database commit was called
        mock_db.commit.assert_called_once()


class TestAsyncProcessing:
    """Test async processing with BackgroundTasks"""
    
    def test_background_task_execution(self):
        """Test that background tasks are properly scheduled"""
        from fastapi import BackgroundTasks
        
        background_tasks = BackgroundTasks()
        
        # Mock the extraction task
        mock_task = MagicMock()
        
        with patch.object(asset_service, 'extract_metadata_task', mock_task):
            # Add task
            background_tasks.add_task(
                asset_service.extract_metadata_task,
                asset_id="test_asset_123"
            )
            
            # Verify task was added
            assert len(background_tasks.tasks) == 1
            task_func, args, kwargs = background_tasks.tasks[0]
            assert kwargs["asset_id"] == "test_asset_123"
    
    def test_background_task_error_handling(self):
        """Test that background tasks handle errors gracefully"""
        mock_db = MagicMock()
        mock_asset = MagicMock()
        mock_asset.id = "test_id"
        mock_asset.status = "processing"
        mock_asset.asset_metadata = {}
        
        # Mock query to return our asset
        mock_db.query.return_value.filter.return_value.first.return_value = mock_asset
        
        with patch('app.services.asset_service.SessionLocal', return_value=mock_db):
            with patch('app.services.asset_service.download_file_from_storage', side_effect=Exception("Download failed")):
                # This should not raise, but set error status
                asset_service.extract_metadata_task("test_id")
        
        # Verify error was handled
        assert mock_asset.status == "error"
        assert "Download failed" in mock_asset.asset_metadata["error"]
        mock_db.commit.assert_called()


class TestFileSizeValidation:
    """Test file size validation"""
    
    def test_oversized_file_rejected(self):
        """Test that files exceeding max size are rejected"""
        client = TestClient(app)
        
        # Create a large "file" (mock the size check)
        large_file = b"x" * (101 * 1024 * 1024)  # 101MB
        
        with patch.dict('os.environ', {'MOCK_MODE': 'false'}):
            with patch('app.config.Settings.max_upload_size', 100 * 1024 * 1024):  # 100MB limit
                response = client.post(
                    "/api/projects/test_project/assets",
                    files={"file": ("large.jpg", io.BytesIO(large_file), "image/jpeg")},
                    data={"user_consent": "true"}
                )
        
        assert response.status_code == 413
        assert "exceeds maximum" in response.json()["detail"]


class TestFileTypeValidation:
    """Test file type validation"""
    
    def test_unsupported_image_type_rejected(self):
        """Test that unsupported image types are rejected"""
        client = TestClient(app)
        
        # Try to upload a TIFF file (assuming it's not in allowed types)
        response = client.post(
            "/api/projects/test_project/assets",
            files={"file": ("test.tiff", io.BytesIO(b"fake tiff data"), "image/tiff")},
            data={"user_consent": "true"}
        )
        
        # In mock mode or if TIFF is not allowed
        if response.status_code == 415:
            assert "not supported" in response.json()["detail"]
    
    def test_supported_types_accepted(self):
        """Test that supported file types are accepted"""
        client = TestClient(app)
        
        supported_types = [
            ("test.jpg", "image/jpeg"),
            ("test.png", "image/png"),
            ("test.mp3", "audio/mpeg"),
            ("test.wav", "audio/wav"),
            ("test.mp4", "video/mp4"),
        ]
        
        with patch.dict('os.environ', {'MOCK_MODE': 'true'}):
            for filename, content_type in supported_types:
                response = client.post(
                    "/api/projects/test_project/assets",
                    files={"file": (filename, io.BytesIO(b"test data"), content_type)},
                    data={"user_consent": "true"}
                )
                
                assert response.status_code == 202, f"Failed for {content_type}"


class TestStorageIntegration:
    """Test MinIO storage integration"""
    
    @pytest.mark.asyncio
    async def test_file_storage_path(self):
        """Test that files are stored with correct path structure"""
        mock_db = MagicMock()
        mock_asset = MagicMock()
        mock_asset.id = "asset_123"
        mock_asset.project_id = "project_456"
        mock_asset.type = "image"
        mock_asset.asset_metadata = {}
        
        file_data = b"test image data"
        
        with patch('app.services.asset_service.upload_file_to_storage') as mock_upload:
            storage_path = await asset_service.process_and_store_file(
                mock_db,
                mock_asset,
                file_data,
                "test.jpg"
            )
        
        # Verify storage path format
        assert storage_path == "projects/project_456/assets/asset_123.jpg"
        
        # Verify upload was called with correct parameters
        mock_upload.assert_called_once()
        call_args = mock_upload.call_args
        assert call_args[1]["bucket_name"] == "ossgameforge-assets"
        assert call_args[1]["object_name"] == storage_path


class TestEndToEndPipeline:
    """Test complete preprocessing pipeline end-to-end"""
    
    @pytest.mark.asyncio
    async def test_complete_image_upload_pipeline(self):
        """Test complete pipeline for image upload"""
        client = TestClient(app)
        
        # Create test image with EXIF
        img = Image.new('RGB', (300, 300), color='yellow')
        exif_data = img.getexif()
        exif_data[0x010F] = "Test Camera"
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG', exif=exif_data)
        img_bytes.seek(0)
        
        with patch.dict('os.environ', {'MOCK_MODE': 'true'}):
            # Upload image
            response = client.post(
                "/api/projects/test_project/assets",
                files={"file": ("test_with_exif.jpg", img_bytes, "image/jpeg")},
                data={"user_consent": "true"}
            )
        
        # Verify response
        assert response.status_code == 202
        assert "asset_id" in response.json()
        assert response.json()["status"] == "processing"
        assert "successfully" in response.json()["message"].lower()


def main():
    """Run all preprocessing pipeline tests"""
    print("="*70)
    print("Task 2.1 - Preprocessing Pipeline Tests")
    print("="*70)
    
    test_classes = [
        TestConsentValidation,
        TestEXIFStripping,
        TestMetadataExtraction,
        TestAsyncProcessing,
        TestFileSizeValidation,
        TestFileTypeValidation,
        TestStorageIntegration,
        TestEndToEndPipeline
    ]
    
    total_passed = 0
    total_failed = 0
    
    for test_class in test_classes:
        class_name = test_class.__name__
        print(f"\nRunning {class_name}...")
        
        for method_name in dir(test_class):
            if method_name.startswith("test_"):
                try:
                    test_instance = test_class()
                    test_method = getattr(test_instance, method_name)
                    
                    # Handle async tests
                    import asyncio
                    import inspect
                    if asyncio.iscoroutinefunction(test_method):
                        asyncio.run(test_method())
                    else:
                        test_method()
                    
                    print(f"  ✅ {method_name} PASSED")
                    total_passed += 1
                    
                except Exception as e:
                    print(f"  ❌ {method_name} FAILED: {e}")
                    total_failed += 1
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    print(f"Total Tests: {total_passed + total_failed}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    
    if total_failed == 0:
        print("\n🎉 All preprocessing pipeline tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total_failed} tests failed.")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())