import twint

c = twint.Config()

c.Search = "Kcorp"

c.Since = "2022-10-14"

c.Utc = True
c.Full_text = False

twint.run.Search(c)