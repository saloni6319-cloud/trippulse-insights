import pandas as pd
from constants import DESTINATIONS


def generate_destinations():

    df = pd.DataFrame(DESTINATIONS)

    df["preferred_seasons"] = df["preferred_seasons"].apply(
        lambda x: ", ".join(x)
    )

    df.insert(0, "destination_id", range(1, len(df) + 1))

    df.to_csv("output/destinations.csv", index=False)

    print("destinations.csv generated successfully!")