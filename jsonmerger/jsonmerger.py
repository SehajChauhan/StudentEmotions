import boto3
def lambda_handler(x, y):

    scrapeyear = x['scrapeyear']
    scrapetype = x['scrapetype']
    prefixer = scrapeyear + "/" + scrapetype + "/"
    finalfile = scrapeyear + scrapetype

    s31 = boto3.client('s3')
    s32 = boto3.resource('s3')
    keys = []
    resp = s31.list_objects_v2(Bucket="convscraper", Prefix= (prefixer))
    for obj in resp['Contents']:
        keys.append(obj['Key'])


    gdata = ""
    for i in range (len(keys)):
        globals()['f%sdata' % i] = ""
        obj = s32.Object('convscraper', keys[i])
        globals()['f%s' % i] = obj.get()['Body'].read().decode('utf-8')
        globals()['f%sdata' % i] = globals()['f%s' % i]
        globals()['f%sdata' % i] = globals()['f%sdata' % i][1:-1]
        gdata += globals()['f%sdata' % i]
        if (i<(len(keys)-1)):
            gdata +=","
    gdata = "{" + gdata + "}"

    result = s32.Object('convscraper', 'json/%s.json' % finalfile)
    result.put(Body=gdata)
