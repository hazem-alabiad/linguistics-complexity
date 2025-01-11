import os
import csv
import string
import syllables


def calculate_statistics(file_path, file_name):
    with open(file_path, "r") as file:
        content = file.read()

        # Split content into sentences
        sentences = content.split(".")
        num_sentences = len([s for s in sentences if s.strip() != ""])

        # Remove punctuation
        content = content.translate(str.maketrans("", "", string.punctuation + "—"))


        # Split content into words
        words = content.split()
        num_words = len(words)

        # Calculate the number of syllables
        syllable_count = 0
        for word in words:
            syllable_count += syllables.estimate(word)

        return {
            "File": file_name,
            "N.Sentences": num_sentences,
            "N.words": num_words,
            "N.syllables": syllable_count,
            "Words.Per.Sentence": round(num_words / num_sentences, 3),
            "Syllables.Per.Word": round(syllable_count / num_words, 3),
            "Grade.Score": round(
            0.39 * (num_words / num_sentences) + 11.8 * (syllable_count / num_words) - 15.59, 3
            ),
        }


def main():
    input_directory = input("Please enter the input directory: ") 
    output_file = input("Please enter the name of the output file: ") 

    print(f"Input Directory: {input_directory}")
    print(f"Output File: {output_file}")

    # Get the statistics for each file in the input directory
    statistics = []
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        file_stats = calculate_statistics(file_path, file_name)
        statistics.append(file_stats)

    # Sort by File
    statistics = sorted(statistics, key=lambda x: int(x["File"].split(".")[0]))

    # Write the statistics to the output file
    with open(output_file + ".csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=statistics[0].keys())
        writer.writeheader()
        for stats in statistics:
            writer.writerow(stats)


if __name__ == "__main__":
    main()
