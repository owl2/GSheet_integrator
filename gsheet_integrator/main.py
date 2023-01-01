from connectors.gsheet import GSheet

def gsheet_extraction():
    gsheet_extract = GSheet()
    df = gsheet_extract.gsheet_extract(SAMPLE_SPREADSHEET_ID="", SAMPLE_RANGE_NAME="Data")

    return df

def main():
    print("Step 1: Extract data from GSheet to S3.")
    gsheet_df = gsheet_extraction()


if __name__ == "__main__":
    main()
