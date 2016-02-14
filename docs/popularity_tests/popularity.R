library(plotly)

min_pop <- 1
max_pop <- 10
terms_n <- 30
step <- 5

inc <- function(x, t=1) { eval.parent(substitute(x <- x + t)) }
dec <- function(x, t=1) { eval.parent(substitute(x <- x - t)) }

make_graph <- function(data) {
    n <- length(data)
    ud1 <- sort(unique(data))
    ud2 <- sort(unique(data))
    plot(1:n, (data[1:n]), main=cat("step =", step), type="p")
    lines(1:n, rep(mean(ud1), n), col="purple")
    inc(ud2[sample(1:length(ud2), 1)], step)
    lines(1:n, rep(mean(ud2), n), col="blue")
    # lines(1:n, rep(mean(data), n), col="red")
}

make_plotly_graph <- function(test_data) {
	count_test <- length(test_data)
    ud1 <- sort(unique(test_data))
    ud2 <- sort(unique(test_data))
	x <- 1:count_test
	y <- test_data
	df <- data.frame(x, y)
	names(df) <- c("n", "popularity")
	p <- plot_ly(df, x=n, y=popularity, name="popularity") %>%
	add_trace(y=rep(mean(ud1), count_test), name="before")
    cat(ud1, "\n")
	inc(ud2[length(ud2)], step)
    cat(ud2, "\n")
	p <- p %>%
    add_trace(y=rep(mean(ud2), count_test), name=paste("after adding", step))
	return (p)
}

# cat("Number of terms:\n")
n <- terms_n
# n <- scan("", n=1)
d <- sample(min_pop:max_pop, n, replace=T)
# d <- scan("", n=n)
summary(d)
p <- make_plotly_graph(d)
p
