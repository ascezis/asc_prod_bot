import React from "react";
import { Box, VStack, Button } from "@chakra-ui/react";

function Sidebar() {
  return (
    <Box w="200px" bg="gray.100" p={4}>
      <VStack spacing={4} align="stretch">
        <Button>Dashboard</Button>
        <Button>Clients</Button>
        <Button>Projects</Button>
      </VStack>
    </Box>
  );
}

export default Sidebar;
