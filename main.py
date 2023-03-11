from data import Data
from data import get_df_list
import os


# WebDriver and app location
driver_binary_location = "/usr/bin/chromedriver"
binary_app_location = "/usr/bin/chromium-browser"

# Having the starting and ending match number same as from server
# (matches are 15735 - 15765)
match_start_num = 15735
match_end_num = 15765

# Removing existing csv data file if it exists
if os.path.exists("data_file.csv"):
    os.remove("data_file.csv")
    print("Removed the existing csv file")

# Looping through the matches and appending the data to a csv
for match_num in range(match_start_num, match_end_num + 1):
    prime_volley_obj = Data()

    # Getting the raw tabular data, cleaning it, rearranging it by each stat
    # (attack, block etc)
    prime_volley_obj.rearrange_list_by_stats(prime_volley_obj.clean_list(
        get_df_list(match_num, driv_bin_loc=driver_binary_location,
                    bin_loc=binary_app_location)), match_no=match_num % 15734)

    # Renaming the columns to unique and intuitive column names
    # (Attacks_finished, Attacking_errors, attacking efficiency etc)
    prime_volley_obj.rename_columns()

    # Merging all the columns to one big file for each match
    prime_volley_obj.merge_everything()

    # Checking if its the first match, if so adding headers to the csv file,
    # else just appending the data without header
    if match_num == match_start_num:
        prime_volley_obj.final_merged_stats.to_csv("data_file.csv", mode='a',
                                                   header=True, index=False,
                                                   na_rep=0)
        print(f"successfully written {match_num} to csv file")
    else:
        prime_volley_obj.final_merged_stats.to_csv("data_file.csv", mode='a',
                                                   header=False, index=False,
                                                   na_rep=0)
        print(f"successfully written {match_num} to csv file")

print("\nSuccessfully written all the matches to the csv file")
