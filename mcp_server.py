from mcp.server.fastmcp import FastMCP
from typing import List


mcp = FastMCP("restock")


@mcp.tool()
def query_top_sku_restock(classid:str) -> List:
        """
        根据SKU类别,查询补货系统近1个月内销量最高的30个SKU
         Args:
                page:一次需要查询页的数量
                pageSize:每页有多少SKU
                classid:商品类型，C002 = 镜架，C003= 镜片
                storeCode: 门店ID
        Returns:
                List: 补货系统中销量前30的商品数组，数组元素的属性为（商品编码，销售数量）

        """
        print("enter tool:query_top_sku_restock")
        return[
                {
  "barcode": "0000138294",
  "salesVolume": 500
}, {
  "barcode": "0000138295",
  "salesVolume": 400
}, {
  "barcode": "0000138296",
  "salesVolume": 300
}, {
  "barcode": "0000138297",
  "salesVolume": 200
}, {
  "barcode": "0000138298",
  "salesVolume": 100
} 
        ]
@mcp.tool()
def query_sku_base(page:int,pageSize:int,storeCode:str,classid:str) -> List:
        """
        根据门店ID，查询此门店必须要有的SKU和对应数量
         Args:
                page:一次需要查询页的数量
                pageSize:每页有多少SKU
                classid:商品类型，C002 = 镜架，C003= 镜片
                storeCode: 门店ID
        Returns:
                List: SKU按页标识的数组，数组元素的属性为（商品品牌，基础数量）
        """
        print("enter tool:query_sku_base")

        return [
{
  "page": 1,
  "pagesize": 100,
  "data": [
    {
      "attr": "暴龙",
      "fixedQuantity": 10
    },
    {
      "attr": "夏蒙",
      "fixedQuantity": 10
    },
    {
      "attr": "ZELE",
      "fixedQuantity": 10
    }
  ]
}
        ]
@mcp.tool()
def query_new_sku_stock(page:int,pageSize:int,classid:str) -> List:
        """ 
        根据商品SKU类别，查询在总部仓库中，一个月内有哪些新品
        Args:
                page:一次需要查询页的数量
                pageSize:每页有多少SKU
                classid:商品类型，C002 = 镜架，C003= 镜片

        Returns:
                List:新品SKU按页标识的数组，数组元素的属性为（商品编码，商品品牌，库存数量，入库时间）
        """
        print("enter tool:query_new_sku_stock")

        return [
                {
                "page": 1,
                        "pagesize": 100,
                                "data": [
                                        {
                "barcode": "0000138293",
      "attr": "夏蒙",
      "quantity": 10,
      "time": "2025-11-05 10:10:10"
    },
    {
      "barcode": "0000138294",
      "attr": "暴龙",
      "quantity": 10,
      "time": "2025-11-05 10:11:10"
    },
    {
      "barcode": "0000138295",
      "attr": "暴龙",
      "quantity": 10,
      "time": "2025-11-05 10:12:10"
    },
    {
      "barcode": "0000138296",
      "attr": "暴龙",
      "quantity": 10,
      "time": "2025-11-05 10:13:10"
    },
    {
      "barcode": "0000138297",
      "attr": "ZELE",
      "quantity": 10,
      "time": "2025-11-05 10:14:10"
    }
  ]}
        ]



@mcp.tool()
def query_top_sku(storeCode:str,classid:str) -> List:
        """ 
        根据门店ID，查询此门店近1个月销量前30的商品
        Args:
                storeCode: 门店ID
                classid:商品类型，C002 = 镜架，C003= 镜片

        Returns:
                List: 门店销量前30的商品数组，数组元素的属性为（商品编码，销售数量）
 
        """
        print("enter tool:query_top_sku")
        return [{
                "barcode":"0000138294",
                "salesVolume":100
        },{
                "barcode":"0000138295",
                "salesVolume":150
        },{
                "barcode":"0000138296",
                "salesVolume":1090
        },{
                "barcode":"0000138297",
                "salesVolume":1200
        },{
                "barcode": "0000138298",
                "salesVolume": 100
}  
        ]

@mcp.tool()
def query_store_sku(storeCode:str,classid:str) -> List:
        """
    根据门店ID，查询门店SKU商品信息和对应的库存情况

    Args:
        storeCode: 门店ID
        classid:商品类型，C002 = 镜架，C003= 镜片

    Returns:
        List: 门店商品的数组，数组元素的属性为（商品编码，商品品牌，库存数量）
        """
        print("enter tool:query_store_sku")

        return [{
                "barcode":"0000138293",
                "attr":"夏蒙",
                "quantity":10
        },{
                "barcode":"0000138294",
                "attr":"暴龙",
                "quantity":2
        },{
                "barcode":"0000138295",
                "attr":"暴龙",
                "quantity":120
        },
        {
                "barcode": "0000138296",
                "attr": "暴龙",
                "quantity": 10
  },
        {
                "barcode":"0000138297",
                "attr":"ZELE",
                "quantity":10
        },
        ]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")