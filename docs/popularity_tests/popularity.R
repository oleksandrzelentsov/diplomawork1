inc <- function(x, t=1) { eval.parent(substitute(x <- x + t)) }
dec <- function(x, t=1) { eval.parent(substitute(x <- x - t)) }

make_graph <- function(data) {
    n <- length(data)
    ud <- sort(unique(data))
    plot(1:n, (data[1:n]), type="p")
    lines(1:n, rep(mean(ud), n), col="purple")
    inc(ud[length(ud)], 50)
    lines(1:n, rep(mean(ud), n), col="blue")
    # lines(1:n, rep(mean(data), n), col="red")
}

# cat("Number of terms:\n")
n <- 10
# n <- scan("", n=1)
d <- sample(rep(1:100, each=n/10))
# d <- scan("", n=n)
summary(d)
make_graph(d)
