import sys
import re

file_path = r'C:\Users\eljoker\Documents\GitHub\toDus-API\todus\stanzas\group.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix signatures for message stanzas
content = re.sub(r'caption: str = "", msg_id: str = ""\) -> str:', 'caption: str = "", msg_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'thumbnail: str, \n                        caption: str = "", msg_id: str = ""\) -> str:', 'thumbnail: str, \n                        caption: str = "", msg_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'thumbnail: str, caption: str = "", msg_id: str = ""\) -> str:', 'thumbnail: str, caption: str = "", msg_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'sticker_pack: str, sticker_hash: str, \n                          msg_id: str = ""\) -> str:', 'sticker_pack: str, sticker_hash: str, \n                          msg_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'contact_phone: str, msg_id: str = ""\) -> str:', 'contact_phone: str, msg_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'edit_id: str = ""\) -> str:', 'edit_id: str = "", reply_to: str = "") -> str:', content)
content = re.sub(r'group_delete_message\(to: str, message_id: str, msg_id: str = "", body: str = "", media_xml: str = ""\) -> str:', 'group_delete_message(to: str, message_id: str, msg_id: str = "", body: str = "", media_xml: str = "", reply_to: str = "") -> str:', content)


# List of functions that should NOT have reply_xml
funcs_to_clean = [
    'group_update_name',
    'group_update_subject',
    'group_update_avatar',
    'group_update_avatar_thumbnail',
    'group_leave_iq',
    'group_get_link_iq',
    'group_set_link_iq',
    'group_get_members_iq',
    'group_set_members_iq'
]

# We will just do string replacement for the exact lines in those functions
for func in funcs_to_clean:
    # Find the function block
    start_idx = content.find(f"def {func}")
    if start_idx == -1: continue
    end_idx = content.find("def ", start_idx + 5)
    if end_idx == -1: end_idx = len(content)
    
    block = content[start_idx:end_idx]
    # Remove the reply_xml line
    block = re.sub(r'\s*reply_xml = f"<reply xmlns=\'reply:n\' mi=\'\{reply_to\}\'/>" if reply_to else ""\n', '\n', block)
    # Remove the injection of {reply_xml}
    block = block.replace("f\"{reply_xml}\"\n", "")
    block = block.replace("f\"{reply_xml}\"", "")
    
    content = content[:start_idx] + block + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done!')
