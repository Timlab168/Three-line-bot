export type ProductId = 8 | 9 | 10 | 11;
export const PRODUCT_NAME: Record<ProductId, string> = {
  8: "Visage Super Serum｜神經美美容精華",
  9: "Pure Cleanse｜淨潤洗面乳",
  10: "Radiant Toner｜煥采化妝水",
  11: "Visage Crème Caviar｜奢華保濕霜"
};
export const PRODUCT_ALIASES: Record<ProductId, string[]> = {
  8: ["8","產品8","Serum","Super Serum","精華","神經美"],
  9: ["9","產品9","Cleanse","Pure Cleanse","洗面乳","清潔"],
  10:["10","產品10","Toner","Radiant Toner","化妝水","保濕"],
  11:["11","產品11","Crème","Cream","Caviar","奢華保濕霜","面霜"]
};
const IMG = {
  8: "https://images.unsplash.com/photo-1586380034382-9f83cf53f36f?w=1200",
  9: "https://images.unsplash.com/photo-1556228453-efd1b4e5e0c4?w=1200",
  10:"https://images.unsplash.com/photo-1600180758890-6b94519a8baa?w=1200",
  11:"https://images.unsplash.com/photo-1610041321721-7a624ba9ae54?w=1200"
};
export function flexForProduct(p: ProductId) {
  const name = PRODUCT_NAME[p];
  const hero = IMG[p];
  const bullets: string[] =
    p===8?["減少皺紋與表情紋","提升水分與彈性","提升整體膚況與幸福感"]:
    p===9?["溫和清潔、去除雜質","滋潤保濕、柔嫩平滑","加強後續保養吸收"]:
    p===10?["平衡 pH 強化屏障","深層補水整日清新","緊緻毛孔、提升吸收力"]:
           ["深層滋養修護","維持彈性與水潤","煥活光澤與保濕"];
  return {
    type:"flex", altText:name,
    contents:{
      type:"bubble",
      hero:{type:"image",url:hero,size:"full",aspectRatio:"16:9",aspectMode:"cover"},
      body:{type:"box",layout:"vertical",contents:[
        {type:"text",text:name,weight:"bold",size:"md",wrap:true},
        {type:"box",layout:"vertical",margin:"sm",spacing:"sm",
         contents:bullets.map(b=>({type:"box",layout:"baseline",spacing:"sm",
           contents:[{type:"text",text:"•",flex:0},{type:"text",text:b,wrap:true,size:"sm",color:"#666"}]}))}
      ]},
      footer:{type:"box",layout:"vertical",spacing:"sm",
        contents:[{type:"button",style:"link",height:"sm",
          action:{type:"uri",label:"更多資訊",uri:"https://example.com/"}}],flex:0}
    }
  };
}
