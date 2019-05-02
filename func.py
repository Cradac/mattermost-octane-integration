import settings, requests, json
from markdownify import markdownify as md

def format_message(j_t):
    #format text if the event type is create
    message = ""
    change_list = ['severity', 'blocked', 'blocked_reason', 'name', 'description', 'defect_type']
    data = j_t['data'][0]['entity']
    if j_t['event_type'] == 'create':
        #Head of Message
        message = f"\
[`{data['name']}`\[{data['id']}\] Defect Erstellt](https://almoctane-eur.saas.hpe.com/ui/entity-navigation?p={j_t['sharedspace_id']}/{j_t['workspace_id']}&entityType=work_item&id={data['id']})\n\
Erkannt von **{data['detected_by']['email'].split('@',1)[0]}**\n\
> {md(data['description'])}"

        if data['blocked'] and data['blocked_reason']:
            message += f"\n**Blocked** wegen {data['blocked_reason']}."
        elif data['blocked'] and not data['blocked_reason']:
            message += f'\n**Blocked.**'

    #format text if the event type is create
    elif j_t['event_type'] == 'update':
        significant_change = False
        #Head of Message
        message = f"\
[`{data['name']}`\[{data['id']}\] Defect Bearbeitet](https://almoctane-eur.saas.hpe.com/ui/entity-navigation?p={j_t['sharedspace_id']}/{j_t['workspace_id']}&entityType=work_item&id={data['id']})\n\
Erkannt von **{data['detected_by']['email'].split('@',1)[0]}**\n\
**Veränderungen:**\n\
"
        for change_name, change_value in j_t['data'][0]['changes'].items():
            if change_name in change_list:
                message += f"* **{change_name}:** "
                significant_change = True
                if change_name == 'severity' or change_name == 'defect_type':
                    message += f"    {change_value['oldValue']['id'].split('.')[2].rstrip()} :arrow_right: {change_value['newValue']['id'].split('.')[2].rstrip()}\n"
                else:
                    message += f"    {md(change_value['oldValue']).rstrip()} :arrow_right: {md(change_value['newValue']).rstrip()}\n"
        if not significant_change:
            return None


#format text if the event type is create
    elif j_t['event_type'] == 'delete':
        #Head of Message
        message = f"\
[`{data['name']}`\[{data['id']}\] Defect Gelöscht](https://almoctane-eur.saas.hpe.com/ui/entity-navigation?p={j_t['sharedspace_id']}/{j_t['workspace_id']}&entityType=work_item&id={data['id']})\n\
> {md(data['description'])}"

    #return message to main function to be sent
    return message





def post_to_mattermost(message, url):
    payload = {
        'text': message
    }
    if settings.mm_channel:
        payload['channel'] = settings.mm_channel
    if settings.mm_username:
        payload['username'] = settings.mm_username
    if settings.mm_profileimage:
        payload['icon_url'] = settings.mm_profileimage
    print(json.dumps(payload, indent=4, sort_keys=True))
    request = requests.post(url, json=payload)


