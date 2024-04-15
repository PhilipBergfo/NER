# Set the working directory
setwd("C:/Users/Admin/Desktop/fixingweatherdata")

# Read the dataset
weather_data <- read.csv("cleaned_weather_data")

# Multiply precipitation by 10000
weather_data$precipitation <- weather_data$precipitation * 10000

# Print the updated dataset
print(weather_data)

# If you want to save the updated dataset to a new CSV file
write.csv(weather_data, "updated_weather_data.csv", row.names = FALSE)
