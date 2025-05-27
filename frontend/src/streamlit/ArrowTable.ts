import { Table, Type } from "apache-arrow";

type CellType = "blank" | "index" | "columns" | "data";

export interface ArrowDataframeProto {
  data: ArrowTableProto;
  height: string;
  width: string;
}

export interface ArrowTableProto {
  data: Uint8Array;
  index: Uint8Array;
  columns: Uint8Array;
  styler: Styler;
}

interface Cell {
  classNames: string;
  content: string;
  id?: string;
  type: CellType;
}

interface Styler {
  caption?: string;
  displayValuesTable: Table;
  styles?: string;
  uuid: string;
}

export class ArrowTable {
  private readonly dataTable: Table;
  private readonly indexTable: Table;
  private readonly columnsTable: Table;
  private readonly styler?: Styler;

  constructor(
    dataBuffer: Uint8Array,
    indexBuffer: Uint8Array,
    columnsBuffer: Uint8Array,
    styler?: any
  ) {
    this.dataTable = Table.from(dataBuffer);
    this.indexTable = Table.from(indexBuffer);
    this.columnsTable = Table.from(columnsBuffer);
    this.styler = styler
      ? {
          caption: styler.get("caption"),
          displayValuesTable: Table.from(styler.get("displayValues")),
          styles: styler.get("styles"),
          uuid: styler.get("uuid"),
        }
      : undefined;
  }

  get rows(): number {
    return this.indexTable.length + this.columnsTable.numCols;
  }

  get columns(): number {
    return this.indexTable.numCols + this.columnsTable.length;
  }

  get headerRows(): number {
    return this.rows - this.dataRows;
  }

  get headerColumns(): number {
    return this.columns - this.dataColumns;
  }

  get dataRows(): number {
    return this.dataTable.length;
  }

  get dataColumns(): number {
    return this.dataTable.numCols;
  }

  get uuid(): string | undefined {
    return this.styler && this.styler.uuid;
  }

  get caption(): string | undefined {
    return this.styler && this.styler.caption;
  }

  get styles(): string | undefined {
    return this.styler && this.styler.styles;
  }

  get table(): Table {
    return this.dataTable;
  }

  get index(): Table {
    return this.indexTable;
  }

  get columnTable(): Table {
    return this.columnsTable;
  }

  public getCell = (rowIndex: number, columnIndex: number): Cell => {
    const isBlankCell =
      rowIndex < this.headerRows && columnIndex < this.headerColumns;
    const isIndexCell =
      rowIndex >= this.headerRows && columnIndex < this.headerColumns;
    const isColumnsCell =
      rowIndex < this.headerRows && columnIndex >= this.headerColumns;

    if (isBlankCell) {
      const classNames = ["blank"];
      if (columnIndex > 0) {
        classNames.push("level" + rowIndex);
      }

      return {
        type: "blank",
        classNames: classNames.join(" "),
        content: "",
      };
    } else if (isColumnsCell) {
      const dataColumnIndex = columnIndex - this.headerColumns;
      const classNames = [
        "col_heading",
        "level" + rowIndex,
        "col" + dataColumnIndex,
      ];

      return {
        type: "columns",
        classNames: classNames.join(" "),
        content: this.getContent(this.columnsTable, dataColumnIndex, rowIndex),
      };
    } else if (isIndexCell) {
      const dataRowIndex = rowIndex - this.headerRows;
      const classNames = [
        "row_heading",
        "level" + columnIndex,
        "row" + dataRowIndex,
      ];

      return {
        type: "index",
        id: `T_${this.uuid}level${columnIndex}_row${dataRowIndex}`,
        classNames: classNames.join(" "),
        content: this.getContent(this.indexTable, dataRowIndex, columnIndex),
      };
    } else {
      const dataRowIndex = rowIndex - this.headerRows;
      const dataColumnIndex = columnIndex - this.headerColumns;
      const classNames = [
        "data",
        "row" + dataRowIndex,
        "col" + dataColumnIndex,
      ];
      const content = this.styler
        ? this.getContent(
            this.styler.displayValuesTable,
            dataRowIndex,
            dataColumnIndex
          )
        : this.getContent(this.dataTable, dataRowIndex, dataColumnIndex);

      return {
        type: "data",
        id: `T_${this.uuid}row${dataRowIndex}_col${dataColumnIndex}`,
        classNames: classNames.join(" "),
        content,
      };
    }
  };

  public getContent = (
    table: Table,
    rowIndex: number,
    columnIndex: number
  ): any => {
    const column = table.getColumnAt(columnIndex);
    if (column === null) {
      return "";
    }

    const columnTypeId = this.getColumnTypeId(table, columnIndex);
    switch (columnTypeId) {
      case Type.Timestamp: {
        return this.nanosToDate(column.get(rowIndex));
      }
      default: {
        return column.get(rowIndex);
      }
    }
  };

  /* Returns apache-arrow specific typeId of column.*/
  private getColumnTypeId(table: Table, columnIndex: number): Type {
    return table.schema.fields[columnIndex].type.typeId;
  }

  private nanosToDate(nanos: number): Date {
    return new Date(nanos / 1e6);
  }
}
