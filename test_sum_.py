import numpy as np
import pandas as pd

POLLS_FILE = "polls.csv"


def test_intention_mentions_sum():
    polls = load_data(POLLS_FILE)
    process_polls(polls)


def load_data(file_path):
    return pd.read_csv(file_path)


def process_polls(polls):

    for _, poll in polls.iterrows():
        poll_path = get_poll_file_path(poll)
        poll_df = load_data(poll_path)

        print(poll_path)

        # Iterate over each row and check the sum of intention_mention_1 to intention_mention_7
        for index, row in poll_df.iterrows():
            print(index, row)
            intentions_together = row[
                [
                    "intention_mention_1",
                    "intention_mention_2",
                    "intention_mention_3",
                    "intention_mention_4",
                    "intention_mention_5",
                    "intention_mention_6",
                    "intention_mention_7",
                ]
            ]
            print(intentions_together)
            sum_mentions = np.nansum(intentions_together)
            assert sum_mentions == 100, (
                f"Sum of intention mentions in row {index} is not 100, \n"
                f" for poll {poll['poll_id']}, \n"
                f"candidate {row['candidate']}, \n"
                f"population {poll['population']}"
            )


def get_poll_file_path(poll):
    return f"{poll['folder']}/{poll['poll_id']}_{poll['population']}.csv"
