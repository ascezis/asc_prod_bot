import React from "react";
import { Box, Text } from "@chakra-ui/react";

function Navbar() {
  return (
    <Box bg="teal.500" p={4} color="white">
      <Text fontSize="xl" fontWeight="bold">
        Admin Panel
      </Text>
    </Box>
  );
}

export default Navbar;
