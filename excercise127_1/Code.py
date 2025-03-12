import sys
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QLabel, QMessageBox)


class DataApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Value Analysis - Pandas GUI")
        self.resize(800, 500)

        # Load data
        self.df = pd.read_csv('./SampleData2(1).csv')

        # Layout
        self.layout = QVBoxLayout()

        # Table Widget
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.table.cellClicked.connect(self.load_selected_row)  # Sự kiện khi bấm vào bảng
        self.load_data()

        # Input Fields
        self.symbol_input = QLineEdit()
        self.price_input = QLineEdit()
        self.pe_input = QLineEdit()

        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Symbol:"))
        input_layout.addWidget(self.symbol_input)
        input_layout.addWidget(QLabel("Price:"))
        input_layout.addWidget(self.price_input)
        input_layout.addWidget(QLabel("PE:"))
        input_layout.addWidget(self.pe_input)
        self.layout.addLayout(input_layout)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Entry")
        self.update_btn = QPushButton("Update Entry")
        self.sort_btn = QPushButton("Sort by Price")
        self.search_btn = QPushButton("Search & Reduce Price")
        self.delete_btn = QPushButton("Delete Entry")

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.sort_btn)
        btn_layout.addWidget(self.search_btn)
        btn_layout.addWidget(self.delete_btn)
        self.layout.addLayout(btn_layout)

        # Connect Buttons to functions
        self.add_btn.clicked.connect(self.add_entry)
        self.update_btn.clicked.connect(self.update_entry)
        self.sort_btn.clicked.connect(self.sort_data)
        self.search_btn.clicked.connect(self.search_entry)
        self.delete_btn.clicked.connect(self.delete_entry)

        # Set Layout
        self.setLayout(self.layout)

    def load_data(self):
        """Load data into QTableWidget"""
        self.table.setRowCount(len(self.df))
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)

        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                self.table.setItem(row, col, QTableWidgetItem(str(self.df.iat[row, col])))

    def load_selected_row(self, row):
        """Load selected row data into input fields"""
        self.symbol_input.setText(self.table.item(row, 0).text())
        self.price_input.setText(self.table.item(row, 1).text())
        self.pe_input.setText(self.table.item(row, 2).text())

    def add_entry(self):
        """Add a new entry to the table"""
        symbol = self.symbol_input.text().strip()
        price_text = self.price_input.text().strip()
        pe_text = self.pe_input.text().strip()

        if not symbol or not price_text or not pe_text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            price = float(price_text)
            pe = float(pe_text)
            usd = price / 23

            new_row = pd.DataFrame([[symbol, price, pe, usd]], columns=self.df.columns)
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.refresh_table()
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá và PE phải là số hợp lệ!")

    def update_entry(self):
        """Update selected entry in the table"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một sản phẩm để cập nhật!")
            return

        symbol = self.symbol_input.text().strip()
        price_text = self.price_input.text().strip()
        pe_text = self.pe_input.text().strip()

        if not symbol or not price_text or not pe_text:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        try:
            self.df.at[selected_row, "Symbol"] = symbol
            self.df.at[selected_row, "Price"] = float(price_text)
            self.df.at[selected_row, "PE"] = float(pe_text)
            self.df.at[selected_row, "USD"] = float(price_text) / 23
            self.refresh_table()
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Giá và PE phải là số hợp lệ!")

    def sort_data(self):
        """Sort table by Price"""
        self.df = self.df.sort_values(by="Price", ascending=True)
        self.refresh_table()

    def search_entry(self):
        """Search for Symbol and reduce its Price by half"""
        symbol = self.symbol_input.text().strip()
        if not symbol:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập Symbol để tìm kiếm!")
            return

        if symbol in self.df["Symbol"].values:
            self.df.loc[self.df["Symbol"] == symbol, "Price"] /= 2
            self.refresh_table()
            QMessageBox.information(self, "Thành công", f"Giá của {symbol} đã giảm một nửa!")
        else:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy sản phẩm!")

    def delete_entry(self):
        """Delete entry by Symbol"""
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một sản phẩm để xóa!")
            return

        symbol = self.table.item(selected_row, 0).text()
        confirm = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc chắn muốn xóa {symbol}?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if confirm == QMessageBox.StandardButton.Yes:
            self.df = self.df[self.df["Symbol"] != symbol]
            self.refresh_table()
            QMessageBox.information(self, "Thành công", f"Sản phẩm {symbol} đã bị xóa!")

    def refresh_table(self):
        """Refresh the table with updated data"""
        self.table.clearContents()
        self.table.setRowCount(len(self.df))
        for row in range(len(self.df)):
            for col in range(len(self.df.columns)):
                self.table.setItem(row, col, QTableWidgetItem(str(self.df.iat[row, col])))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataApp()
    window.show()
    sys.exit(app.exec())
