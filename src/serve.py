import os
import boto3
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

ARTIFACT_BUCKET = os.environ["ARTIFACT_BUCKET"]
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """Tải file model.joblib từ AWS S3 Bucket về máy khi server khởi động.

    Sử dụng credentials đã cấu hình qua 'aws configure' hoặc môi trường.
    """
    # Tạo thư mục ~/models nếu chưa tồn tại
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # TODO 1 & 2: Khởi tạo client S3
    s3_client = boto3.client("s3")

    # TODO 3: Tải file model từ S3 xuống máy
    s3_client.download_file(
        Bucket=ARTIFACT_BUCKET, Key=MODEL_KEY, Filename=MODEL_PATH
    )

    # TODO 4: In thông báo thành công
    print(f"Model đã được tải xuống từ S3: s3://{ARTIFACT_BUCKET}/{MODEL_KEY}")


download_model()
model = joblib.load(MODEL_PATH)


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """Endpoint kiểm tra sức khỏe server.

    GitHub Actions gọi endpoint này sau khi deploy để xác nhận server đang chạy.
    """
    # TODO 5: Trả về dict {"status": "ok"}
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """Endpoint suy luận chính.

    Đầu vào : JSON {"features": [f1, f2, ..., f10]}
    Đầu ra  : JSON {"prediction": <0|1>, "label":
    <"thu_nhap_thap"|"thu_nhap_cao">}
    """
    # TODO 6: Kiểm tra số lượng đặc trưng
    if len(req.features) != 10:
        raise HTTPException(
            status_code=400,
            detail=f"Cần chính xác 10 đặc trưng, nhận được {len(req.features)}.",
        )

    # TODO 7: Gọi model.predict([req.features]) để lấy kết quả dự đoán
    pred = int(model.predict([req.features])[0])

    # TODO 8: Trả về dict chứa "prediction" (int) và "label" (string)
    label = "thu_nhap_cao" if pred == 1 else "thu_nhap_thap"

    return {"prediction": pred, "label": label}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)