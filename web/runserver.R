library(plumber)
server <- plumb("server.R")
server$run(port=8000)
