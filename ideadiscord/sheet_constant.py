sheet_id = '1vH3KuOfu2w7efJ8kiMTDd_Tj_R2znpATkTKPDbtg7WE'
sheet_name = '第一回通過者'

discord_channel_id = 792794338336964620
discord_role_id = 792792490842783762

num_token_length = 9

column_email = 'B'
column_real_name = 'C'
column_twitter = 'D'
column_number_id = 'F'
column_token = 'G'
column_discord_id = 'H'
column_discord_tag = 'I'


def sheet_column(string):
    return ord(string) - ord('A') + 1
