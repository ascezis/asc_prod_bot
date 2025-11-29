import React from "react";
import { Box, Table, Thead, Tbody, Tr, Th, Td } from "@chakra-ui/react";

function Clients() {
  const clients = [
    { id: 1, name: "John Doe", telegram: 123456789 },
    { id: 2, name: "Jane Smith", telegram: 987654321 }
  ];

  return (
    <Box p={6}>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Name</Th>
            <Th>Telegram ID</Th>
          </Tr>
        </Thead>
        <Tbody>
          {clients.map((c) => (
            <Tr key={c.id}>
              <Td>{c.id}</Td>
              <Td>{c.name}</Td>
              <Td>{c.telegram}</Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
}

export default Clients;
