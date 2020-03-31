library(shiny)
library(plyr)
library(plotly)
library(reshape2)
library(DT)
library(RColorBrewer)


labMap <- read.delim("./labMap.csv", sep = ",")


ui <- fluidPage(

    # Application title
    titlePanel("Demo2"),

    sidebarLayout( 
          sidebarPanel(
            
            selectInput("bars", "Bar Position:",
                        c("Non-stacked" = "nonStack",
                          "Stacked" = "stack")),
              br(),
           
            checkboxGroupInput("lbTest", "Laboratory Test:",
                         choices= list("All" = "All",
                            "white blood cell count (Leukocytes)" = "white blood cell count (Leukocytes)",
                            "neutrophil count" = "neutrophil count", 
                            "lymphocyte count"= "lymphocyte count", 
                            "albumin" = "albumin",
                            "lactate dehydrogenase (LDH)" = "lactate dehydrogenase (LDH)",
                            "alanine aminotransferase (ALT)" = "alanine aminotransferase (ALT)" ,
                            "aspartate aminotransferase (AST)" = "aspartate aminotransferase (AST)",
                            "total bilirubin" = "total bilirubin", 
                            "creatinine" = "creatinine",
                            "C-reactive protein (CRP)" = "C-reactive protein (CRP)",
                            "prothrombin time (PT)" = "prothrombin time (PT)",
                            "procalcitonin" = "procalcitonin", 
                            "D-dimer" = "D-dimer",
                            "cardiac troponin" = "cardiac troponin"
                            ), 
                         selected = "All"),
              br(),
              selectInput("icdVersion", "ICD version:",
                          c("All" = "all",
                            "ICD9" = 9,
                            "ICD10" = 10)), 
              br(), 
              sliderInput("patients", "Number of patients:",
                          min = 0, max = 1000, value = c(0,250)
              )
            
        ),

        mainPanel(
            tabsetPanel(type = "tabs",
                      tabPanel("Daily Counts", plotOutput("dailyCounts")),
                      tabPanel("Demographics", plotOutput("sexByAge"), plotOutput("sexPlot")), 
                      tabPanel("Laboratory", plotOutput("lab")),
                      tabPanel("Diagnosis", plotOutput("diag"),DT::dataTableOutput('icdDesc'), plotOutput("phenoPrevalence"))
                               
                  
      )
        )
        
    )
)

server <- function(input, output) {
    
    dailyCounts <- read.delim(list.files(path = ".", pattern = "DailyCounts"), 
                              header = TRUE, sep = ",")
    #colnames( dailyCounts ) <- c("siteid", "date", "new_positive_cases", 
    #                             "patients_in_icu", "new_deaths")
    mdaily <- melt( dailyCounts)
    
    
    demographics <- read.delim(list.files(path = ".", pattern = "Demographics"), 
                               header = TRUE, sep = ",")
    colnames( demographics ) <- c("siteid", "sex", "total_patients", 
                                  "age_0to2", "age_3to5", "age_6to11", 
                                  "age_12to17", "age_18to25", "age_26to49", 
                                  "age_50to69", "age_70to79", "age_80plus")
    
    mdemog <- melt( demographics)
    
    demogTotal <- mdemog[ mdemog$variable == "total_patients" & mdemog$sex != "All", ]
    demogByAge <- mdemog[ mdemog$variable != "total_patients" & mdemog$sex != "All", ]
    
    laboratory <- read.delim(list.files(path = ".", pattern = "Labs"), 
                             header = TRUE, sep = ",")
    colnames(laboratory) <- c("siteid", "loinc", "days_since_positive", 
                              "num_patients", "mean_value", "stdev_value")
    labMap <- read.delim("./labMap.csv", sep = ",")
    laboratory <- merge( laboratory, labMap)
    
    diagnosis <- read.delim(list.files(path = ".", pattern = "Diagnosis"), 
                            header = TRUE, sep = ",", colClasses = "character")
    colnames(diagnosis) <- c("siteid", "icd_code", "icd_version", "num_patients")
    diagnosis$num_patients <- as.numeric( diagnosis$num_patients)
    
    icdMapping <- read.delim("./mappingICD_CCS", 
                             sep = "\t", 
                             colClasses = "character", 
                             header = TRUE )
    icdMapping$ICDpair <- paste0( icdMapping$ICDcode, "*",icdMapping$ICDversion)
    
    diagnosis$ICDcode <- gsub("[.]", "", diagnosis$icd_code)
    diagnosis$ICDpair <- paste0( diagnosis$ICDcode, "*",diagnosis$icd_version)
    diagnosis <- merge( diagnosis, icdMapping, all.x = TRUE, by = "ICDpair")
    
    diagnosis$pat_num <- ifelse( diagnosis$num_patients < min(diagnosis[ which( diagnosis$num_patients > 0), "num_patients"]),
            paste0("<", min(diagnosis[ which( diagnosis$num_patients > 0), "num_patients"]) ),diagnosis$num_patients)

    diagnosis$num_patients <- ifelse( diagnosis$num_patients < min(diagnosis[ which( diagnosis$num_patients > 0), "num_patients"]),
                                      min(diagnosis[ which( diagnosis$num_patients > 0), "num_patients"])-1,diagnosis$num_patients)
    
    output$dailyCounts <- renderPlot({
        if( input$bars == "nonStack"){
        ggplot(data=mdaily, aes(x=date, y=value, fill=variable)) +
            geom_bar(stat="identity", position=position_dodge()) + 
            theme_bw()+
            theme(axis.text.x = element_text(angle =45, hjust = 1))+
            labs(title = "Daily BCH patient counts", y="number of patients")
        }else{
            ggplot(data=mdaily, aes(x=date, y=value, fill=variable)) +
                geom_bar(stat="identity", position="stack") + 
                theme_bw()+
                theme(axis.text.x = element_text(angle =45, hjust = 1))+
                labs(title = "Daily BCH patient counts", y="number of patients")
          
            
            
        }
    })
    
    output$sexPlot <- renderPlot({
        ggplot(demogTotal, aes(x="", y=value, fill=sex)) +
        geom_bar(stat="identity", width=1) +
        coord_polar("y", start=0)+ theme_void()
     })
    
    output$sexByAge <- renderPlot({
        if( input$bars == "nonStack"){
            ggplot(data=demogByAge[demogByAge$sex !="All",], aes(x=variable, y=value, fill=sex)) +
                geom_bar(stat="identity", position=position_dodge()) + 
                theme(axis.text.x = element_text(angle =45, hjust = 1))+theme_bw()+
            labs(title = "Distribution by Age and Sex in BCH", y="number of patients")
          
        }else{
            ggplot(data=demogByAge[demogByAge$sex !="All",], aes(x=variable, y=value, fill=sex)) +
                geom_bar(stat="identity", position=("stack")) + 
                theme(axis.text.x = element_text(angle =45, hjust = 1))+theme_bw()+
            labs(title = "Distribution by Age and Sex in BCH", y="number of patients")
          
            
        }
           })
    
    output$lab <- renderPlot({
      if( input$lbTest == "All"){
        ggplot(data=laboratory, aes(x=days_since_positive, 
                                    y=mean_value, 
                                    group=labTest)) +
          geom_line(aes(col=labTest))+
          geom_point() + theme(legend.position="bottom", legend.direction="vertical")+
          labs(title = "Lab test mean value in BCH", 
               x = "days since positive", y = "lab test mean value")
        
        
      }else{
        laboratorySelection <- laboratory[ laboratory$labTest == input$lbTest,]
        ggplot(data=laboratorySelection, aes(x=days_since_positive, 
                                    y=mean_value, 
                                    group=labTest)) +
          geom_line(aes(col=labTest))+
          geom_point() + theme(legend.position="bottom", legend.direction="vertical")+
          labs(title = "Lab test mean value in BCH", 
               x = "days since positive", y = "lab test mean value")

        
      }
            })
    
    output$diag <- renderPlot({
      
      diagnosis <- diagnosis[ diagnosis$num_patients >= input$patients[1] & 
                                diagnosis$num_patients <= input$patients[2], ]
  
        if( input$icdVersion != "all"){
            diagSelection <- diagnosis[ diagnosis$icd_version == input$icdVersion, ]
            ggplot(data=diagSelection, aes(x=reorder(icd_code,-num_patients), y=num_patients)) +
                geom_bar(stat="identity", position=position_dodge()) + 
                theme(axis.text.x = element_text(angle =45, hjust = 1))+
              labs(title = "Number of patients by ICD9/ICD10 code in BCH", 
                   x = "ICD9/ICD10 code", y = "number of patients")
            
          }else{
            ggplot(data=diagnosis, aes(x=reorder(icd_code,-num_patients), y=num_patients)) +
                geom_bar(stat="identity", position=position_dodge()) + 
                theme(axis.text.x = element_text(angle =45, hjust = 1))+
              labs(title = "Number of patients by ICD9/ICD10 code in BCH", 
                   x = "ICD9/ICD10 code", y = "number of patients")
            
        }
    })
    output$icdDesc <- DT::renderDataTable(
      
      if( input$icdVersion != "all"){
        diagnosis <- diagnosis[ diagnosis$num_patients >= input$patients[1] & 
                                  diagnosis$num_patients <= input$patients[2], ]
        doutp <- diagnosis[ diagnosis$ICDversion == input$icdVersion,  c("num_patients","icd_code", "ICDdescription", "ICDversion")]
        colnames(doutp) <- c("NumberOfPatients", "ICDcode", "ICDdescription", "ICDversion")
        doutp[ order( doutp$NumberOfPatients, decreasing = TRUE), ]
      }
      else{
        diagnosis <- diagnosis[ diagnosis$num_patients >= input$patients[1] & 
                                  diagnosis$num_patients <= input$patients[2], ]
        doutp <- diagnosis[, c("num_patients","icd_code", "ICDdescription", "ICDversion")]
        colnames(doutp) <- c("NumberOfPatients", "ICDcode", "ICDdescription", "ICDversion")
        doutp[ order( doutp$NumberOfPatients, decreasing = TRUE), ]
      }
      ,rownames = FALSE)
    
    output$phenoPrevalence <- renderPlot({
      if( input$icdVersion != "all"){
        diagSelection <- diagnosis[ diagnosis$icd_version == input$icdVersion, ]
        freq <- as.data.frame(table(diagSelection$Category))
        freq$Perc <- freq$Freq/nrow(freq)*100
        
        ggplot( data=freq, aes( x=reorder(Var1,-Freq), y=freq$Perc))+ geom_bar(stat="identity")+
          labs(x = "Phenotype category", 
               y = "Percentage", 
               title  = "Percentage of ICD by phenotype category")+
          theme(axis.text.x = element_text(angle =45, hjust = 1))
      
        #ggplot(data=freq, aes(x="", y=Perc, fill=Var1)) +
        #  geom_bar(stat="identity", width=1, color="white") +
        #  coord_polar("y", start=0) +
          
        #  theme_void() 
    #  }else{
    #    mappingSelection <- icdMapping[ icdMapping$ICDcode %in% diagnosis$icd_code, c(1,2,4) ]
    #    freq <- as.data.frame(table(mappingSelection$Phenotype))
    #    freq$Perc <- freq$Freq/nrow(freq)*100
        
    #    ggplot( data=freq, aes( x=reorder(Var1,-Freq), y=freq$Perc))+ geom_bar(stat="identity")+
    #      labs(x = "Phenotype category", 
    #           y = "Percentage", 
    #           title  = "Percentage of ICD by phenotype category")+
    #      theme(axis.text.x = element_text(angle =45, hjust = 1))
        
     }
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
