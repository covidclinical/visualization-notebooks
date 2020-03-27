##file 1  DailyCounts-SiteID.csv
#Fields: siteid, date, new_positive_cases, patients_in_icu, new_deaths
#Notes:
#(1) One row per date (2020-03-15, 2020-03-16, etc.)
#(2) Site is a unique identifier for your institution (e.g., "BIDMC")
#(3) new_positive_cases, patients_in_icu, and new_deaths are number of distinct patients
#(4) If a patient has multiple positive test results, use the earliest date
#(5) Set patients_in_icu = -2 if you do not have ICU data
#(6) Set new_deaths = -2 if you do not have death data
#(7) Obfuscate small counts with "-1" as required by your institution

dailyCounts <- as.data.frame( matrix( ncol=5, nrow=32))
colnames( dailyCounts ) <- c("siteid", "date", "new_positive_cases", 
                             "patients_in_icu", "new_deaths")

dailyCounts["siteid"] <- "BCH"
dailyCounts["date"] <- seq(as.Date("2020-03-20"), as.Date("2020-04-20"), "days")
dailyCounts["new_positive_cases"] <- sort( sample(1:100, 32, replace=FALSE))
dailyCounts["patients_in_icu"] <- sort( sample(1:50, 32, replace=FALSE))
dailyCounts["new_deaths"] <- -2
  
write.table( dailyCounts, file="/Users/alba/Desktop/DailyCounts-BCH.csv", 
             col.names = TRUE, row.names = FALSE, quote = FALSE, sep = ",")


#File #2: Demographics-SiteID.csv
#Fields: siteid, sex, total_patients, age_0to2, age_3to5, age_6to11, age_12to17, age_18to25, age_26to49, age_50to69, age_70to79, age_80plus
#Notes:
#(1) One row per sex (values = "Male", "Female", "Other", "All")
#(2) Count anyone who is not male or female as "Other"
#(3) Include all patients in the "All" row
#(4) The total_patients value in the sex=All row should be everyone
#(5) Obfuscate small counts with "-1" as required by your institution

demographics <- as.data.frame( matrix( ncol=12, nrow=4))
colnames( demographics ) <- c("siteid", "sex", "total_patients", 
                             "age_0to2", "age_3to5", "age_6to11", 
                             "age_12to17", "age_18to25", "age_26to49", 
                             "age_50to69", "age_70to79", "age_80plus")

demographics["siteid"] <- "BCH"
demographics["sex"] <- c("Male", "Female", "Other", "All")
demographics["total_patients"] <- c(round(0.6*sum(dailyCounts$new_positive_cases)), sum(dailyCounts$new_positive_cases)-round(0.6*sum(dailyCounts$new_positive_cases)), 0, sum(dailyCounts$new_positive_cases))
