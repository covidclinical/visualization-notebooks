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
  
write.table( dailyCounts, file="./DailyCounts-SiteID.csv", 
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

#I enter the numbers manually to match with the sum and follow a progression
demographics[1,4:12] <- c(0,5,8,12,60,135,246,303,340)
demographics[2,4:12] <- c(0,0,7,12,34,89,149,195,253)
demographics[3,4:12] <- 0
demographics[4,4:12] <- colSums(demographics[1:3,4:12])


write.table( demographics, file="./Demographics-SiteID.csv", 
             col.names = TRUE, row.names = FALSE, quote = FALSE, sep = ",")


#File #3: Labs-SiteID.csv
#Fields: siteid, loinc, days_since_positive, num_patients, mean_value, stdev_value
#Notes:
#(1) One row per loinc and days_since_positive
#(2) days_since_positive = 1 on the date the patient has a positive COVID test result
#(3) Start the table at days_since_positive = -6 (seven days before the positive test)
#(4) Go for as many days as you have data: days_since_positive = 5, 6, 7, ...
#(5) Map your local loinc codes to the loinc code in Gabe's list
#(6) Only use Gabe's loinc codes in this list, not your local codes
#(7) Obfuscate small counts with "-1" as required by your institution

write.table( labs, file="./Labs-SiteID.csv", 
             col.names = TRUE, row.names = FALSE, quote = FALSE, sep = ",")


#File #4: Diagnoses-SiteID.csv
#Fields: siteid, icd_code, icd_version, num_patients
#Notes:
#(1) One row per ICD diagnosis code
#(2) All diagnoses the patients have starting seven days before the positive test 
#(3) icd_version = "9" or "10"
#(4) Obfuscate small counts with "-1" as required by your institution
#Examples: (Diagnoses-BIDMC.csv)


write.table( diagnoses, file="./Diagnoses-SiteID.csv", 
             col.names = TRUE, row.names = FALSE, quote = FALSE, sep = ",")

