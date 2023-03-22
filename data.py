import pandas as pd
from selenium import webdriver


# Getting the unfiltered data from the website, Finding the tables in it,
# converting them to a list of pandas DFs.
def get_df_list(match_no: int, bin_loc, driv_bin_loc) -> list:

    # Having 3 tries for the selenium module to load the whole page so as to
    # avoid timeout and to
    # avoid No Tables ValueError
    for tries in range(3):
        try:
            options = webdriver.ChromeOptions()
            options.binary_location = bin_loc
            chrome_driver_binary = driv_bin_loc
            browser = webdriver.Chrome(chrome_driver_binary,
                                       chrome_options=options)
            browser.get(f"https://en.volleyballworld.com/volleyball/"
                        f"competitions/prime-volleyball-league-2023/schedule/"
                        f"{match_no}/#boxscore")
            html_gotten = browser.page_source
            browser.close()
            df_list = pd.read_html(html_gotten)
            return df_list
        # In case if it closes before fully loading the Table, this tries
        # again. Also prints the failed match number
        except ValueError:
            print(f"trying match number {match_no} again")


# For getting the standings data and writing it to csv.
def make_standings_file(bin_loc, driv_bin_loc) -> None:
    # Having 3 tries for the selenium module to load the whole page so as to
    # avoid timeout and to
    # avoid No Tables ValueError
    for tries in range(3):
        try:
            options = webdriver.ChromeOptions()
            options.binary_location = bin_loc
            chrome_driver_binary = driv_bin_loc
            browser = webdriver.Chrome(chrome_driver_binary,
                                       chrome_options=options)
            browser.get("https://en.volleyballworld.com/volleyball/"
                        "competitions/prime-volleyball-league-2023/"
                        "standings/")
            html_gotten_standings = browser.page_source
            browser.close()
            pd.read_html(html_gotten_standings)[0].to_csv("standings.csv")
            print("Successfully written standings data to csv")
            return None

        # In case if it closes before fully loading the Table, this tries
        # again. Also prints the failed match number
        except ValueError:
            print(f"trying to get league standings again")


class Data:

    def __init__(self):
        # Placeholder for the two team names to iterate through
        self.team_a = None
        self.team_b = None
        self.combined_attack_stats = pd.DataFrame()
        self.combined_block_stats = pd.DataFrame()
        self.combined_serve_stats = pd.DataFrame()
        self.combined_reception_stats = pd.DataFrame()
        self.combined_libero_stats = pd.DataFrame()
        self.combined_setter_stats = pd.DataFrame()
        self.final_merged_stats = pd.DataFrame()

    def clean_list(self, df_list: list) -> list:
        # List of indexes of the stats to remove. i.e., All set stats, All
        # stats combined (Aggregated Stats)
        # In the case that a 5 set match was played
        if len(df_list) == 85:
            to_remove = [1, 2, 3, 4, 5, 6, 7, 8, 15, 22, 29, 36, 43, 44, 45,
                         46, 47, 48, 49, 50, 57, 64, 71, 78]
        # In case a 4 set match was played
        elif len(df_list) == 71:
            to_remove = [1, 2, 3, 4, 5, 6, 7, 8, 15, 22, 29, 36, 37, 38, 39,
                         40, 41, 42, 43, 50, 57, 64]
        # In case a straight 3 set match was played
        elif len(df_list) == 57:
            to_remove = [1, 2, 3, 4, 5, 6, 7, 8, 15, 22, 29, 30, 31, 32, 33,
                         34, 35, 36, 43, 50]

        # Removing the unwanted aggregated stats from the df list. reversing
        # the list to avoid index out of range
        # error while deleting items
        for df_index in to_remove[::-1]:
            del df_list[df_index]

        # Popping the main aggregated stats (index 0) which contains team names
        # and assigning it to the below variables
        temp_stats = df_list.pop(0)
        # [:-3] to remove the three letter Short Team Name at the end of these
        # column names - Kolkata ThunderboltsKOL
        self.team_a = temp_stats.columns[0][:-3]
        self.team_b = temp_stats.columns[3][:-3]

        return df_list

    def rearrange_list_by_stats(self, df_list: list, match_no: int) -> None:
        # Attack, Block, Serve, Reception, Libero, Setter
        for i, df in enumerate(df_list):
            # Because there are 60 DFs. Sets go from 1 - 10 after the below
            # code. But for semi finals that are played less than 5 sets, there
            # are 36 or 48 DFs. then sets go from 1 - 6 or 8. i.e, 3 or 4 set.
            set_num = (i // 6) + 1
            # Adding Set Numbers to all the Stats to merge them correctly
            if len(df_list) == 60:
                df['Set'] = set_num if set_num <= 5 else set_num - 5
            elif len(df_list) == 48:
                df['Set'] = set_num if set_num <= 4 else set_num - 4
            elif len(df_list) == 36:
                df['Set'] = set_num if set_num <= 3 else set_num - 3
            # Checking the order of the DF to determine what type it is, i.e.,
            # attack, block, serve etc
            if i % 6 == 0:
                # If the set <= half the total sets then its from left team and
                # if its > half the total sets played it's from right
                # team. (the right side team reduces by half of the len of
                # total sets to get the set number correct.
                # Also for right team switches the order of teams to get the
                # Playing Team and Opponents correct.
                if set_num <= (len(df_list) // 6) // 2:
                    df['Team'], df['Opponent'], df['Match Number'] = \
                        (self.team_a, self.team_b, match_no)
                else:
                    df['Team'], df['Opponent'], df['Match Number'] = \
                        (self.team_b, self.team_a, match_no)
                self.combined_attack_stats = pd.concat(
                    [self.combined_attack_stats, df], axis=0,
                    ignore_index=True)
            # There are no extra columns being added for the rest of the stats
            # because only 1 stat DF should have extra columns when merging.
            # Otherwise there will be 6 team, opponent columns each.
            elif i % 6 == 1:
                self.combined_block_stats = pd.concat(
                    [self.combined_block_stats, df], axis=0, ignore_index=True)
            elif i % 6 == 2:
                self.combined_serve_stats = pd.concat(
                    [self.combined_serve_stats, df], axis=0, ignore_index=True)
            elif i % 6 == 3:
                self.combined_reception_stats = pd.concat(
                    [self.combined_reception_stats, df], axis=0,
                    ignore_index=True)
            elif i % 6 == 4:
                self.combined_libero_stats = pd.concat(
                    [self.combined_libero_stats, df], axis=0,
                    ignore_index=True)
            elif i % 6 == 5:
                self.combined_setter_stats = pd.concat(
                    [self.combined_setter_stats, df], axis=0,
                    ignore_index=True)

    def rename_columns(self) -> None:
        self.combined_attack_stats.columns = ['jersey_no', 'player_name',
                                              'position', 'successful_attacks',
                                              'attacking_errors',
                                              'attacks_unfinished',
                                              'total_attacks',
                                              'attacking_efficiency', 'set',
                                              'team', 'opponent',
                                              'match_number']
        self.combined_block_stats.columns = ['jersey_no', 'player_name',
                                             'position', 'successful_blocks',
                                             'blocking_errors', 'touches',
                                             'total_blocks',
                                             'blocking_efficiency', 'set']
        self.combined_serve_stats.columns = ['jersey_no', 'player_name',
                                             'position', 'service_ace',
                                             'service_errors',
                                             'serves_in_play', 'total_serves',
                                             'service_efficiency', 'set']
        self.combined_reception_stats.columns = ['jersey_no', 'player_name',
                                                 'position',
                                                 'successful_receives',
                                                 'reception_errors',
                                                 'receives_kept_in_play',
                                                 'total_receives',
                                                 'reception_efficiency', 'set']
        self.combined_libero_stats.columns = ['jersey_no', 'player_name',
                                              'position', 'successful_digs',
                                              'dig_errors',
                                              'total_digs', 'dig_efficiency',
                                              'set']
        self.combined_setter_stats.columns = ['jersey_no', 'player_name',
                                              'position',
                                              'successful_dumps/pumps',
                                              'setting_errors',
                                              'sets_to_attackers',
                                              'total_sets',
                                              'setting_efficiency',
                                              'set']

    # Merges all the separate stats to one final variable containing all the
    # stats (to export to csv later)
    def merge_everything(self) -> None:
        self.final_merged_stats = pd.merge(self.combined_attack_stats,
                                           self.combined_block_stats,
                                           on=('set', 'player_name',
                                               'jersey_no', 'position'))
        self.final_merged_stats = pd.merge(self.final_merged_stats,
                                           self.combined_serve_stats,
                                           on=('set', 'player_name',
                                               'jersey_no', 'position'))
        self.final_merged_stats = pd.merge(self.final_merged_stats,
                                           self.combined_reception_stats,
                                           on=('set', 'player_name',
                                               'jersey_no', 'position'))
        self.final_merged_stats = pd.merge(self.final_merged_stats,
                                           self.combined_libero_stats,
                                           on=('set', 'player_name',
                                               'jersey_no', 'position'))
        self.final_merged_stats = pd.merge(self.final_merged_stats,
                                           self.combined_setter_stats,
                                           on=('set', 'player_name',
                                               'jersey_no', 'position'))
