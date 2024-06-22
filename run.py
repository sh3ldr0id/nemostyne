from app import bot

if __name__ == "__main__":
    print("Server Running !")

    bot.polling()

    print("Server Stopped !")
    
    # while True:
    #     try:
    #         print("Server Running !")

    #         bot.polling()

    #         print("Server Stopped !")
            
    #         break

    #     except Exception as e:
    #         print(e)