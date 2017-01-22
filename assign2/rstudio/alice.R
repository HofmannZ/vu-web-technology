# source('crawler.R')

read_plain_text <- function(filename) {
  f <- file(filename,'r')
  t <- paste(readLines(f),sep="")
  close(f)
  t
}

split <- function(text, splitstr = "^CHAPTER") {
  chapter_indexes <- grep(splitstr, text, value=FALSE)
  chapter_names <- grep("^CHAPTER", text, value=TRUE)
  if (chapter_indexes[1] > 1) {
    # text before the first chapter
    chapter_indexes <- append(0,chapter_indexes)
    chapter_names <- append("prefix",chapter_names)
  }
  chapters <- list()
  segments <- cbind(chapter_indexes+1,append(chapter_indexes[-1]-1,length(text)))
  for(r in seq(1,length(chapter_indexes))) {
    print(paste("Selecting from",segments[r,1],"to",segments[r,2]))
    chapters <- append(chapters,list(text[segments[r,1]:segments[r,2]]))
  }
  names(chapters) <- chapter_names
  chapters
}

tokenize <- function(text) {
  print("Tokenizing")
  terms <- unlist(strsplit(text,'\\W'))
  lowercase <- tolower(terms)
  lowercase <- lowercase[which(lowercase!="")]
  freq_table <- table(lowercase)
  rm(terms)
  tokens <- sort(lowercase[!duplicated(lowercase)])
  list(dict=freq_table,tokens=tokens,all_tokens=lowercase)
}

process_alice <- function(text, chapters, tf="irr") {
  dicts <- list()
  for (c in chapters) {
    ctokenized <- tokenize(c)
    dicts <- append(dicts,list(ctokenized$dict))
  }
  names(dicts) <- names(chapters)
  print("Starting analysis")
  dist <- tokenize(text)
  tfm <- get_tf_matrix(dist$tokens,dicts)
  idfm <- compute_idf(tfm)
  print("Computing tfidf")
  tfidfm <- compute_tfidf(tfm,tf)
  list(total=dist,names=names(chapters),tfm=tfm,idfm=idfm,tfidfm=tfidfm)
}

process_wikipedia_results <- function(phrase, wikibase="http://simple.wikipedia.org", limit=50, tf="irr") {
  URL <- paste(wikibase,'/w/index.php?title=Special%3ASearch&profile=default&limit=',limit,'&fulltext=Search&search=',curlEscape(c(phrase)), sep='')
  dom <- get(URL)
  anchors <- get_attrs(dom,'//div[@class="mw-search-result-heading"]/a')
  alltext <- ""
  urls <- c()
  dicts <- list()
  for(a in anchors[1,]) {
    aURL <- absolute_wiki_url(a,URL)
    print(aURL)
    adom <- get(aURL)
    atext <- get_wiki_body_content(adom)
    atokenized <- tokenize(atext) 
    alltext <- append(alltext,atext)
    urls <- append(urls,aURL)
    dicts <- append(dicts,list(atokenized$dict))
  }
  print("Starting analysis")
  dist <- tokenize(alltext)
  tfm <- get_tf_matrix(dist$tokens,dicts)
  idfm <- compute_idf(tfm)
  print("Computing tfidf")
  tfidfm <- compute_tfidf(tfm,tf)
  list(total=dist,names=urls,tfm=tfm,idfm=idfm,tfidfm=tfidfm)
}

get_tf_matrix <- function(tokens, dicts) {
  print("Building Term Frequency matrix")
  print(paste("Token list length:",length(tokens)))
  ut <- unique(tokens)
  nt <- length(ut)
  nd <- length(dicts)
  tfm <- matrix(rep(0,nt*nd),nrow=nt)
  row.names(tfm) <- ut
  for (d in seq(1,length(dicts))) {
    cat("DICT",d,"\n")
    for (t in names(dicts[[d]])) {
      tfm[t,d] <- dicts[[d]][[t]]
    }
  }
  print("Done")
  tfm
}

# tf.idf implementation as in Introduction to Information Retrieval
compute_tf_iir <- function(tdim) {
  log(1+tdim)
}
# tf.idf implementation as in Wikipedia
compute_tf_wikipedia <- function(tdim) {
  tdim / apply(tdim,1,max)
}
compute_idf <- function(tdim) {
  log(ncol(tdim) / rowSums(ifelse(tdim>0,1,0)))
}

compute_tfidf <- function(tdim,tf="irr") {
  ( if(tf=="irr") { 
      compute_tf_iir(tdim) 
    } else { 
      compute_tf_wikipedia(tdim)
    }
  ) * compute_idf(tdim)
}

search <- function(query,names,tfidf_matrix) {
  # split query string by whitespace
  q <- unlist(strsplit(query,"\\s+"))
  # discard unknown query terms
  q <- q[which(q %in% rownames(tfidf_matrix))]
  # compute document weights
  weights <- round(colSums(matrix(tfidf_matrix[q,],
                                  ncol=length(names))),digits=2)
  names(weights) <- names
  sort(weights,decreasing=TRUE)
} 

zipf <- function(dist) {
  z <- sort(dist$dict,decreasing=TRUE)
  plot.default(z,log='xy',xlab='rank',ylab='frequency')
  z
}

heaps <- function(dist) {
  u <- rep(1,length(dist$all_tokens))
  for (i in seq(1,length(dist$all_tokens))) {
    u[i] <- length(unique(dist$all_tokens[1:i]))
  }
  plot(u,xlab="input tokens",ylab="dictionary size")
  u
}

fit_heaps <- function(heaps) {
  T <- seq(1,length(heaps))
  M <- heaps
  fit <- nls(M~k*T^b, start=list(k=30,b=0.5))
  k <- coef(fit)[['k']]
  b <- coef(fit)[['b']]
  list(M=k*T^b, k=k, b=b)
}
