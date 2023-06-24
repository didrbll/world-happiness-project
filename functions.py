def create_region_column(output_df, input_df, field):
    regions = {}
    for output_row in output_df.iterrows():
        output_index = output_row[0]
        output_country = output_row[1][field]
        for row15 in input_df.iterrows():
            country15 = row15[1]['Country']
            if country15 == output_country:
                region = row15[1]['Region']
                regions[output_index] = region
                break
        if output_index not in regions:
            regions[output_index] = 'Unknown'
    output_df['Region'] = regions
