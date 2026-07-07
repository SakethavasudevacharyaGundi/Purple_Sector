from pathlib import Path

from ml.traffic.traffic_loss_trainer import (
    TrafficLossTrainer,
)


def main():

    trainer = (
        TrafficLossTrainer()
    )

    (
        model,
        mae,
        X_test,
        y_test,
        predictions,
    ) = trainer.train(
        "data/ml/v1/traffic_loss_dataset.parquet"
    )

    model_dir = Path(
        "data/ml/models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        model_dir /
        "traffic_loss_model.cbm"
    )

    model.save_model(
        model_path
    )

    print()

    print(
        f"Final MAE: {mae:.4f}"
    )

    print(
        f"Saved: {model_path}"
    )


if __name__ == "__main__":
    main()