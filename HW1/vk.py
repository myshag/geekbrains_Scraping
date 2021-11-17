with open("./token.data","r+") as token_file:
    token=token_file.readline()

def exec_api(method:str,token:str,params:dict=None,version="5.131"):
    api_url = "https://api.vk.com/method/"
    rParams = { 
       "access_token": token,
        "v":version
    }
    if not params is None:
        rParams.update(params)
    result=requests.get(api_url+method,params=rParams)
    return result.json()


par = {
    
 "user_ids":"1",
    "fields":" photo_id, verified, sex, bdate, city, country, home_town, has_photo, photo_50, photo_100, photo_200_orig, photo_200, photo_400_orig, photo_max, photo_max_orig, online,"
    
}
exec_api("users.get",vk_api_key,par)