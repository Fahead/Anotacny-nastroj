Co treba zmenit v kode ked to bude na servery
1) premennu 'filename' ktora je vo funkcii load_path(), tam treba dat absolutnu cestu textaku priecinky.txt v ktorom budu napisane cesty ku priecinkom
2) premenna pom v hlavnej funkcii hello(), pomocnej treba zmenit cislo kolko znakov ma odrzerat aby dalej program vedel otvorit dane adresary
3) do txt subora priecinky.txt ktory sa nachadza v priecinku kde je program treba napisat vsetky cesty ku priecinkam v tvare ako to mam ja na lokale
4) python flask umoznuje pristupovat iba k obrazkom ktore su v priecinku static, takze tam treba ukladat obrazky
5) defaultne python flask uz ma povolene threading, ale napisal som ho pre istotu aj do app.run(threaded=True)
