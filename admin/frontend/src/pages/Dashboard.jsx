import React, { useEffect, useState } from "react";
import {
  Box,
  Heading,
  Grid,
  GridItem,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Text,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  Spinner,
  Flex,
} from "@chakra-ui/react";
import { getStatistics } from "../api/statistics";
import { motion } from "framer-motion";

const MotionBox = motion(Box);

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      const data = await getStatistics();
      setStats(data);
    } catch (err) {
      console.error("Ошибка загрузки статистики:", err);
      setError("Не удалось загрузить статистику");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Flex justify="center" align="center" minH="50vh">
        <Spinner size="xl" />
      </Flex>
    );
  }

  if (error || !stats) {
    return (
      <Box>
        <Heading size="lg" mb={6}>
          Dashboard
        </Heading>
        <Text color="red.500">{error || "Нет данных"}</Text>
      </Box>
    );
  }

  const getStatusColor = (status) => {
    const colors = {
      new: "blue",
      in_progress: "yellow",
      completed: "green",
      rejected: "red",
    };
    return colors[status] || "gray";
  };

  return (
    <Box>
      <Heading size="lg" mb={6}>
        📊 Dashboard
      </Heading>

      <Grid templateColumns="repeat(4, 1fr)" gap={6} mb={8}>
        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Stat>
            <StatLabel>Всего клиентов</StatLabel>
            <StatNumber>{stats.total_clients}</StatNumber>
          </Stat>
        </MotionBox>

        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Stat>
            <StatLabel>Всего проектов</StatLabel>
            <StatNumber>{stats.total_projects}</StatNumber>
          </Stat>
        </MotionBox>

        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Stat>
            <StatLabel>За последние 7 дней</StatLabel>
            <StatNumber>{stats.recent_projects_count}</StatNumber>
          </Stat>
        </MotionBox>

        <MotionBox
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Stat>
            <StatLabel>Средний AI Score</StatLabel>
            <StatNumber>{stats.average_realism_score}</StatNumber>
            <StatHelpText>из 10</StatHelpText>
          </Stat>
        </MotionBox>
      </Grid>

      <Grid templateColumns="repeat(2, 1fr)" gap={6} mb={8}>
        <MotionBox
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Heading size="md" mb={4}>
            Проекты по статусам
          </Heading>
          {Object.entries(stats.projects_by_status).map(([status, count]) => (
            <Flex key={status} justify="space-between" mb={2}>
              <Badge colorScheme={getStatusColor(status)}>{status}</Badge>
              <Text fontWeight="bold">{count}</Text>
            </Flex>
          ))}
        </MotionBox>

        <MotionBox
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          bg="white"
          _dark={{ bg: "gray.800" }}
          p={6}
          rounded="lg"
          shadow="md"
        >
          <Heading size="md" mb={4}>
            Проекты по типам
          </Heading>
          {Object.entries(stats.projects_by_type)
            .slice(0, 5)
            .map(([type, count]) => (
              <Flex key={type} justify="space-between" mb={2}>
                <Text>{type || "Не указан"}</Text>
                <Text fontWeight="bold">{count}</Text>
              </Flex>
            ))}
        </MotionBox>
      </Grid>

      <MotionBox
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        bg="white"
        _dark={{ bg: "gray.800" }}
        p={6}
        rounded="lg"
        shadow="md"
      >
        <Heading size="md" mb={4}>
          Топ клиентов
        </Heading>
        <Table variant="simple">
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Username</Th>
              <Th>Full Name</Th>
              <Th>Проектов</Th>
            </Tr>
          </Thead>
          <Tbody>
            {stats.top_clients.map((client) => (
              <Tr key={client.id}>
                <Td>{client.id}</Td>
                <Td>@{client.username || "—"}</Td>
                <Td>{client.full_name || "—"}</Td>
                <Td>
                  <Badge colorScheme="blue">{client.projects_count}</Badge>
                </Td>
              </Tr>
            ))}
          </Tbody>
        </Table>
      </MotionBox>
    </Box>
  );
}

export default Dashboard;
