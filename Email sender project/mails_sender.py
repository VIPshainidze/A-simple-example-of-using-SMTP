from csv import DictReader
from smtplib import SMTP
from time import sleep, time

"""
უსაფრთხოების დონის დასაწევი ლინკი ჯიმეილისთის.
https://myaccount.google.com/u/2/lesssecureapps?pli=1&pageId=none
"""


# ფუნგცია აბრუნებს ზუსტად იმავეს რასაც ჩაშენებული len()
def ln(_):
    i = 0
    for __ in _:
        i += 1
    return i


# ფუნგცია აბრუნებს იმავეს რასაც ჩაშენებული round()
def rnd(_, __):
    return float((str(_)[:str(_).find('.')] + str(_)[str(_).find('.'):str(_).find('.')+__+1]))


start_comp = time()

# სამწუხაროდ თუ საბედნიეროდ ადრესანტების მისამართთა და პაროლთა სია ხელითაა შესავსები.
senders_list = ["<<< MAIL ADDRESS HERE >>>"]
passwords_list = ["<<< PASSWORD HERE >>>"]


def main_fun():

    # ფუნგცია უკავშირდება სერვერს და აბრუნებს მრავალჯერადი გამოყენების წვდომას
    def server_configuration(
            address, password
    ):
        global sender, server  # ეს დედამოტყნული მოდულის დონის გააქტიურება ვერსად ვერ ვიპოვე თუ როგორ უნდა.
        sender = address
        # სერვერთან წვდომის კონფიგურაცია
        server = SMTP("smtp.gmail.com", 587)
        server.starttls()

        return server.login(sender, password)

    def main_sender():
        # senders_counter - ადრესანტებთან წვდომის ინდექსი
        # sent_counter - ეს ისედაც იასნია პროსტა აბშიაკში ითვლის და არა კონკრეტულ მეილზე
        senders_counter, sent_counter, not_started = 0, 0, True

        if not_started:  #
            server_configuration(senders_list[senders_counter], passwords_list[senders_counter])
            not_started = False
            senders_counter += 1

        with open("mails_buffer.csv") as csv_file:
            reader = DictReader(csv_file)

            for row in reader:
                sent_counter += 1
                for key, value in row.items():
                    server.sendmail(sender, value, "<<< MAIL CONTENT HERE!!! >>>")
                    print(f"{str(sent_counter)}: შეტყობინება წარმატებით გაიგზავნა ადრესატთან: {value} ადრესანტი: "
                          f"{senders_list[senders_counter]}")

                if sent_counter % 40 == 0:
                    if sent_counter == 400 - 1:  # ყოველ 400-ე გაგზავნის ოპერაციაზე ...
                        sleep(20)  # ... სერვერი "ისვენებს" 20 წამით, რომ დედა არ მაეტყნას.

                    senders_counter += 1

                    if senders_counter <= ln(senders_list) - 1:
                        # ყოველ 40-ე  ოპერაციაზე მეილი იცვლება რო არ წარმოიშვას error 69* - სერვერის დედის ტყვნა
                        server_configuration(senders_list[senders_counter], passwords_list[senders_counter])
                    else:  # შესვენების შემდეგ კვლავ ახლიდან უბრუნდება ადრესანტების სიას.
                        senders_counter = 0
                        server_configuration(senders_list[senders_counter], passwords_list[senders_counter])

    main_sender()


main_fun()

end_comp = time()
"""
დაგზავნის ოპერაციების უმოკლესი დროის პერსპექტივაში ნაკლებია შანსი, რომ ეს ოდესმე დაიპრინტოს. სხვა მხრივ ერთი 
მეილითაც მოხერხდებოდა. +: მეტი ადრესანტი ნაკლები დროისა და შეცდომის წარმოქმნის შანსის გარანტია. 
"""
print(str(rnd(end_comp - start_comp, 5)))
