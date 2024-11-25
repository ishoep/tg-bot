from django.http import JsonResponse
from telegram import Update
from bot.management.commands.startbot import application 

async def bot_webhook(request):
    if request.method == "POST":
        try:
            update = Update.de_json(request.body.decode("utf-8"), application.bot)
            await application.process_update(update)
            return JsonResponse({"status": "ok"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request method"})
