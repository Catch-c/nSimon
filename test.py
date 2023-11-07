import pyperclip
import Database as Database


encryptedcookie = input()
cookie = Database.decrypt_cookie(encryptedcookie)

text_to_copy = cookie

# Set the clipboard content
pyperclip.copy(text_to_copy)
print(cookie)