import mlflow
import pytest


@pytest.fixture(autouse=True)
def override_mlflow_tracking_uri(tmp_path):
  # Ép MLflow sử dụng thư mục tạm do pytest tạo ra thay vì đường dẫn hardcode
  tracking_dir = tmp_path / "mlruns"
  mlflow.set_tracking_uri(f"file://{tracking_dir.as_posix()}")