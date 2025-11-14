import java.security.SecureRandom;


class Main {
    public static void main(String[] args) {
        // Создание генератора
        SecureRandom random = new SecureRandom();

        byte[] bytes = new byte[16];
        random.nextBytes(bytes);

        // Преобразование массива байтов в двоичную строку
        StringBuilder binaryString = new StringBuilder();
        for (byte b : bytes) {
            String binaryByte = String.format("%8s", Integer.toBinaryString(b & 0xFF)).replace(' ', '0');
            binaryString.append(binaryByte);
        }

        System.out.println(binaryString.toString());
    }
}