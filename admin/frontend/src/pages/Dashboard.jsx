import React from "react";
import { Box, Text } from "@chakra-ui/react";

function Dashboard() {
  return (
    <Box p={6}>
      <Text fontSize="2xl" fontWeight="bold">
        Dashboard
      </Text>
      <Text mt={2}>Welcome to your admin panel!</Text>
    </Box>
  );
}

export default Dashboard;
