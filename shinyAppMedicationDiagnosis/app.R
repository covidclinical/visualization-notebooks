library(shiny)
library(ggplot2)
load("./toplot.RData")

ui <- fluidPage(

    titlePanel("Medication - diagnosis"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            selectizeInput("medClassA",
                        "Medication class A:",
                        choices = c("choose" = "", unique( toplot$med_class ))), 
            selectizeInput("medClassB",
                           "Medication class B:",
                           choices = c("choose" = "", unique( toplot$med_class ))),
            selectizeInput("diagGroup",
                        "Diagnostic group:",
                        choices = c("choose" = "", unique( toplot$description )))
            #, 
            #downloadButton('downloadPlot', 'Download Plot')
            

           
        ),
        
        mainPanel(
            splitLayout(cellWidths = c("50%", "50%"), plotOutput("plotMedA"), plotOutput("plotMedB"))
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {
    

    output$plotMedA <- renderPlot({
        datatoplot  <- toplot[ toplot$description == input$diagGroup & 
                                   toplot$med_class == input$medClassA,]

        xlim <- max( toplot[ toplot$description == input$diagGroup, "WithDiagnosis_beforeAdmission" ], na.rm = TRUE)
        ylim <- max( toplot[ toplot$med_class %in% c(input$medClassA, input$medClassB), "OnMedication_beforeAdmission" ], na.rm = TRUE)
        
        #xlim <- max( c( toplot$WithDiagnosis_beforeAdmission), na.rm = TRUE)
        #ylim <- max( c( toplot$OnMedication_beforeAdmission), na.rm = TRUE)
        
        ggplot( data = datatoplot, mapping = aes( x = WithDiagnosis_beforeAdmission, 
                                                  y = OnMedication_beforeAdmission), 
                shape = status) +
            geom_point( aes(shape= factor( status)), size = 2, alpha = 0.5, 
                        color = datatoplot$Country.Color)+
            geom_text(aes(label=siteid),hjust=0, vjust=0, size = 2)+
            theme(legend.position = "bottom", 
                  plot.title = element_text(hjust = 0.5, size = 10), 
                  axis.title.x = element_text(size = 8), 
                  axis.title.y = element_text(size = 8))+
        scale_y_continuous(name= paste0( "% (patients on ", input$medClassA," / total severe status patients)*100"), limits=c(0, ylim)) +
            scale_x_continuous(name= paste0( "% (patients with ", input$diagGroup, " / total severe status patients)*100" ), limits=c(0, xlim)) +
            labs(title= paste0( input$medClassA, " - ", input$diagGroup), shape = "Severity status" )
    })
    
    output$plotMedB <- renderPlot({
        datatoplot  <- toplot[ toplot$description == input$diagGroup & 
                                   toplot$med_class == input$medClassB,]
        
        xlim <- max( toplot[ toplot$description == input$diagGroup, "WithDiagnosis_beforeAdmission" ], na.rm = TRUE)
        ylim <- max( toplot[ toplot$med_class %in% c(input$medClassA, input$medClassB), "OnMedication_beforeAdmission" ], na.rm = TRUE)
        
        #xlim <- max( c( toplot$WithDiagnosis_beforeAdmission), na.rm = TRUE)
        #ylim <- max( c( toplot$OnMedication_beforeAdmission), na.rm = TRUE)
        
        ggplot( data = datatoplot, mapping = aes( x = WithDiagnosis_beforeAdmission, 
                                              y = OnMedication_beforeAdmission), 
                shape = status) +
            geom_point( aes(shape= factor( status)), size = 2, alpha = 0.5, 
                        color = datatoplot$Country.Color)+
            geom_text(aes(label=siteid),hjust=0, vjust=0, size = 2)+
            theme(legend.position = "bottom", 
                  plot.title = element_text(hjust = 0.5, size = 10), 
                  axis.title.x = element_text(size = 8), 
                  axis.title.y = element_text(size = 8))+
            scale_y_continuous(name= paste0( "% (patients on ", input$medClassB," / total severe status patients)*100"), limits=c(0, ylim+1)) +
            scale_x_continuous(name= paste0( "% (patients with ", input$diagGroup, " / total severe status patients)*100" ), limits=c(0, xlim+1)) +
            labs(title= paste0( input$medClassB, " - ", input$diagGroup ), shape = "Severity status")
        
        })

}

# Run the application 
shinyApp(ui = ui, server = server)
