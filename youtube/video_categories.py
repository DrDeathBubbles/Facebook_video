# Sample python code for videoCategories.list

def video_categories_list(client, **kwargs):
  # See full sample for function
  kwargs = remove_empty_kwargs(**kwargs)

  response = client.videoCategories().list(
    **kwargs
  ).execute()

  return print_response(response)

video_categories_list(client,
    part='snippet',
    regionCode='US')