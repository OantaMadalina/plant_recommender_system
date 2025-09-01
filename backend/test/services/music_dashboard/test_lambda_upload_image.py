from test.utils import BOOTCAMP_BUCKET, get_test_file_path, bucket_file_exists


def test_upload_image_ok(s3bucket, bootcamp_bucket):
    from services.music_dashboard.lambda_upload_location_image import upload_location_image_handler

    with open(get_test_file_path("music_dashboard/chillplace.jpg"), "rb") as fh:
        output = fh.read()

    request = {
        "headers": {
            "Content-Type": "multipart/form-data"
        },
        "pathParameters": {"filename": "someimage.png"},
        "body": str(output)
    }

    response = upload_location_image_handler(request, None)

    result = response
    assert result["body"] == "MusicDashboard/Locations/Images/someimage.png"
    assert bucket_file_exists(BOOTCAMP_BUCKET, "MusicDashboard/Locations/Images/someimage.png")
