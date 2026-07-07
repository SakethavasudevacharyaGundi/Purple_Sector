from pathlib import Path

from ml.traffic.overtake_trainer import (
    OvertakeTrainer,
)


def main():

    trainer = (
        OvertakeTrainer()
    )

    (
        model,
        auc,
    ) = trainer.train(
        "data/ml/v1/overtake_dataset.parquet"
    )

    model_dir = Path(
        "data/ml/models"
    )

    model_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        model_dir
        /
        "overtake_model.cbm"
    )

    model.save_model(
        model_path
    )

    print()

    print(
        f"Final AUC: {auc:.4f}"
    )

    print(
        f"Saved: {model_path}"
    )


if __name__ == "__main__":
    main()