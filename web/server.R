library("redux")
redis <- redux::hiredis()

PREFIX = "CANDIDATES"

#* @filter cors
cors <- function(res) {
    res$setHeader("Access-Control-Allow-Origin", "*")
    plumber::forward()
}

#* @post /addCandidate
function(candidate = "", address = "") {
    redis$HSET(PREFIX, address, candidate)
}

#* @get /getCandidates
function() {
    redis$HGETALL(PREFIX)
}
