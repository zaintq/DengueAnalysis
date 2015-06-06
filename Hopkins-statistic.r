#load lat-long dataset
data = read.csv("/Applications/XAMPP/xamppfiles/htdocs/Dengue/irs-pats-coords-2013.txt")

# Generate random dataset
set.seed(123)
n <- nrow(df)
random_df <- data.frame(
  x = runif(nrow(df), min(df$eruptions), max(df$eruptions)),
  y = runif(nrow(df), min(df$waiting), max(df$waiting))
)

library(clustertend)
set.seed(123)
hopkins(data, n=nrow(data)-1)

install.packages("jsonlite", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("mime", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("curl", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("httr", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("memoise", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("digest'", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("git2r", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')

install.packages("devtools", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')

install.packages("digest", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("plyr", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("reshape2", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("scales", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')
install.packages("ggplot2", lib='/Applications/XAMPP/xamppfiles/htdocs/Dengue/r-lib/')