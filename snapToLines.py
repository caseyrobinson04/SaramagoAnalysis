import os
import pandas as pd
import eyekit
import textsE
import csv
from eyekit.fixation import Fixation
from eyekit.text import TextBlock
from eyekit.vis import Image

# Load and sort fixation data
df = pd.read_csv("fixations.csv")
df = df[(df["x"] >= 0) & (df["y"] >= 0)]
df = df.sort_values(by=["trial", "start_time"])

all_trials = []

# Loop through each trial
for trial_id, trial_df in df.groupby("trial"):
    print(f"Processing trial {trial_id}...")


    # Filter for each column within the current trial
    column1_df = trial_df[trial_df["column_id"] == 1]
    column2_df = trial_df[trial_df["column_id"] == 2]

    # Create FixationSequence for each column
    fixations1 = [
        Fixation(index=idx, x=row["x"], y=row["y"],
                start=int(row["start_time"]),
                end=int(row["start_time"]) + int(row["duration"]))
        for idx, row in column1_df.iterrows()
    ]
    column1 = eyekit.FixationSequence(fixations1)

    fixations2 = [
        Fixation(index=idx, x=row["x"], y=row["y"],
                start=int(row["start_time"]),
                end=int(row["start_time"]) + int(row["duration"]))
        for idx, row in column2_df.iterrows()
    ]
    column2 = eyekit.FixationSequence(fixations2)

    # Define text for left and right columns
    left_text = getattr(textsE, f"left_{trial_id}")
    right_text = getattr(textsE, f"right_{trial_id}")

    # Define text blocks
    left_block = TextBlock(
        left_text,
        position=(92, 182),
        font_face='Times New Roman',
        font_size=32,
        line_height=113.5,
        align='left',
        anchor='left'
    )

    right_block = TextBlock(
        right_text,
        position=(1000, 182),
        font_face='Times New Roman',
        font_size=32,
        line_height=113.5,
        align='left',
        anchor='left'
    )

    # Make sure the subfolder exists
    output_dir = "alignment_images"

    # SNAP TO LEFT COLUMN
    img = Image(1920, 1080)
    img.draw_text_block(left_block)
    img.draw_fixation_sequence(column1)
    img.save(os.path.join(output_dir, f"trial{trial_id}_left_before_snap.png"))

    column1.snap_to_lines(left_block, method ='cluster')
    img = Image(1920, 1080)
    img.draw_text_block(left_block)
    img.draw_fixation_sequence(column1)
    img.save(os.path.join(output_dir, f"trial{trial_id}_left_after_snap.png"))

    # SNAP TO RIGHT COLUMN
    img = Image(1920, 1080)
    img.draw_text_block(right_block)
    img.draw_fixation_sequence(column2)
    img.save(os.path.join(output_dir, f"trial{trial_id}_right_before_snap.png"))

    column2.snap_to_lines(right_block, method=['merge', 'slice', 'cluster', 'warp'])
    img = Image(1920, 1080)
    img.draw_text_block(right_block)
    img.draw_fixation_sequence(column2)
    img.save(os.path.join(output_dir, f"trial{trial_id}_right_after_snap.png"))

# Convert fixations back to a DataFrame
def fixation_seq_to_df(fix_seq, trial_id, column_id):
    return pd.DataFrame([{
        "trial": trial_id,
        "index": f.index,
        "start_time": f.start,
        "end_time": f.end,
        "x": f.x,
        "y": f.y,  # updated Y coord
        "duration": f.end - f.start,
        "column_id": column_id
    } for f in fix_seq])

    # Combine both columns’ snapped fixations
    column1_df = fixation_seq_to_df(column1, trial_id, column_id=1)
    column2_df = fixation_seq_to_df(column2, trial_id, column_id=2)
    combined_df = pd.concat([column1_df, column2_df])

    all_trials.append(combined_df)

# Combine all trial DataFrames into one
final_df = pd.concat(all_trials)

final_df.to_csv(os.path.join(output_dir, "all_trials_snapped_fixations.csv"), index=False)