import React, { useState, useEffect } from "react";
import {
  Box,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Button,
  Input,
  Select,
  HStack,
  VStack,
  Heading,
  Badge,
  IconButton,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  FormControl,
  FormLabel,
  useDisclosure,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
} from "@chakra-ui/react";
import { EditIcon, DeleteIcon } from "@chakra-ui/icons";
import { getUsers, updateUser, deleteUser } from "../api/users";
import { getUser, getCurrentUser } from "../api/auth";

function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [search, setSearch] = useState("");
  const [roleFilter, setRoleFilter] = useState("");
  const [selectedUser, setSelectedUser] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const toast = useToast();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const {
    isOpen: isDeleteOpen,
    onOpen: onDeleteOpen,
    onClose: onDeleteClose,
  } = useDisclosure();
  const cancelRef = React.useRef();

  useEffect(() => {
    loadUsers();
    loadCurrentUser();
  }, [search, roleFilter]);

  const loadCurrentUser = async () => {
    try {
      // Сначала пробуем получить из localStorage
      const localUser = getUser();
      if (localUser) {
        setCurrentUser(localUser);
      } else {
        // Если нет в localStorage, запрашиваем с сервера
        const user = await getCurrentUser();
        setCurrentUser(user);
      }
    } catch (err) {
      console.error("Failed to load current user:", err);
      // Fallback на localStorage
      const localUser = getUser();
      if (localUser) {
        setCurrentUser(localUser);
      }
    }
  };

  const loadUsers = async () => {
    setLoading(true);
    try {
      const data = await getUsers(search || null, roleFilter || null);
      setUsers(data);
    } catch (err) {
      toast({
        title: "Ошибка",
        description: err.response?.data?.detail || "Не удалось загрузить пользователей",
        status: "error",
        duration: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (user) => {
    setSelectedUser({ ...user });
    onOpen();
  };

  const handleSave = async () => {
    try {
      await updateUser(selectedUser.id, {
        email: selectedUser.email,
        role: selectedUser.role,
        is_active: selectedUser.is_active,
      });
      toast({
        title: "Успешно",
        description: "Пользователь обновлен",
        status: "success",
        duration: 3000,
      });
      onClose();
      loadUsers();
    } catch (err) {
      toast({
        title: "Ошибка",
        description: err.response?.data?.detail || "Не удалось обновить пользователя",
        status: "error",
        duration: 3000,
      });
    }
  };

  const handleDelete = async () => {
    try {
      await deleteUser(selectedUser.id);
      toast({
        title: "Успешно",
        description: "Пользователь удален",
        status: "success",
        duration: 3000,
      });
      onDeleteClose();
      loadUsers();
    } catch (err) {
      toast({
        title: "Ошибка",
        description: err.response?.data?.detail || "Не удалось удалить пользователя",
        status: "error",
        duration: 3000,
      });
    }
  };

  const getRoleBadgeColor = (role) => {
    switch (role) {
      case "owner":
        return "purple";
      case "admin":
        return "blue";
      case "user":
        return "green";
      default:
        return "gray";
    }
  };

  const canEditRole = () => {
    return currentUser?.role === "owner";
  };

  const canDelete = () => {
    return currentUser?.role === "owner" && selectedUser?.id !== currentUser?.id;
  };

  return (
    <Box>
      <VStack spacing={4} align="stretch">
        <Heading size="lg">Управление пользователями</Heading>

        <HStack spacing={4}>
          <Input
            placeholder="Поиск по username или email..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            maxW="300px"
          />
          <Select
            placeholder="Все роли"
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            maxW="200px"
          >
            <option value="user">User</option>
            <option value="admin">Admin</option>
            <option value="owner">Owner</option>
          </Select>
          <Button onClick={loadUsers} isLoading={loading}>
            Обновить
          </Button>
        </HStack>

        <Box overflowX="auto">
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>ID</Th>
                <Th>Username</Th>
                <Th>Email</Th>
                <Th>Роль</Th>
                <Th>Статус</Th>
                <Th>Действия</Th>
              </Tr>
            </Thead>
            <Tbody>
              {users.map((user) => (
                <Tr key={user.id}>
                  <Td>{user.id}</Td>
                  <Td>{user.username}</Td>
                  <Td>{user.email}</Td>
                  <Td>
                    <Badge colorScheme={getRoleBadgeColor(user.role)}>
                      {user.role}
                    </Badge>
                  </Td>
                  <Td>
                    <Badge colorScheme={user.is_active ? "green" : "red"}>
                      {user.is_active ? "Активен" : "Неактивен"}
                    </Badge>
                  </Td>
                  <Td>
                    <HStack spacing={2}>
                      <IconButton
                        icon={<EditIcon />}
                        size="sm"
                        onClick={() => handleEdit(user)}
                        aria-label="Редактировать"
                      />
                      {canDelete() && (
                        <IconButton
                          icon={<DeleteIcon />}
                          size="sm"
                          colorScheme="red"
                          onClick={() => {
                            setSelectedUser(user);
                            onDeleteOpen();
                          }}
                          aria-label="Удалить"
                        />
                      )}
                    </HStack>
                  </Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>
      </VStack>

      {/* Модальное окно редактирования */}
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Редактировать пользователя</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {selectedUser && (
              <VStack spacing={4}>
                <FormControl>
                  <FormLabel>Username</FormLabel>
                  <Input value={selectedUser.username} isReadOnly />
                </FormControl>
                <FormControl>
                  <FormLabel>Email</FormLabel>
                  <Input
                    value={selectedUser.email}
                    onChange={(e) =>
                      setSelectedUser({ ...selectedUser, email: e.target.value })
                    }
                  />
                </FormControl>
                {canEditRole() && (
                  <FormControl>
                    <FormLabel>Роль</FormLabel>
                    <Select
                      value={selectedUser.role}
                      onChange={(e) =>
                        setSelectedUser({ ...selectedUser, role: e.target.value })
                      }
                    >
                      <option value="user">User</option>
                      <option value="admin">Admin</option>
                      <option value="owner">Owner</option>
                    </Select>
                  </FormControl>
                )}
                {canEditRole() && (
                  <FormControl>
                    <FormLabel>Статус</FormLabel>
                    <Select
                      value={selectedUser.is_active ? "active" : "inactive"}
                      onChange={(e) =>
                        setSelectedUser({
                          ...selectedUser,
                          is_active: e.target.value === "active",
                        })
                      }
                    >
                      <option value="active">Активен</option>
                      <option value="inactive">Неактивен</option>
                    </Select>
                  </FormControl>
                )}
                <Button colorScheme="blue" onClick={handleSave} width="100%">
                  Сохранить
                </Button>
              </VStack>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>

      {/* Диалог подтверждения удаления */}
      <AlertDialog
        isOpen={isDeleteOpen}
        leastDestructiveRef={cancelRef}
        onClose={onDeleteClose}
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Удалить пользователя
            </AlertDialogHeader>
            <AlertDialogBody>
              Вы уверены, что хотите удалить пользователя "{selectedUser?.username}"?
              Это действие нельзя отменить.
            </AlertDialogBody>
            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={onDeleteClose}>
                Отмена
              </Button>
              <Button colorScheme="red" onClick={handleDelete} ml={3}>
                Удалить
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  );
}

export default Users;

