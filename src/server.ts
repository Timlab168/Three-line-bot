import 'dotenv/config';
import express from 'express';
import morgan from 'morgan';
import { middleware, Client, WebhookEvent, Message } from '@line/bot-sdk';
import { PRODUCT_ALIASES, PRODUCT_NAME, flexForProduct, ProductId } from './lib/flex.js';

const config = {
  channelAccessToken: process.env.CHANNEL_ACCESS_TOKEN || '',
  channelSecret: process.env.CHANNEL_SECRET || ''
};
const client = new Client(config as any);
const app = express();
app.use(morgan('tiny'));
app.get('/', (_, res) => res.type('text').send('THREE bot up'));
app.use('/public', express.static('public'));
app.post('/webhook', middleware(config as any), async (req, res) => {
  const events = req.body.events as WebhookEvent[];
  await Promise.all(events.map(handleEvent));
  res.sendStatus(200);
});
async function handleEvent(event: WebhookEvent): Promise<void> {
  if (event.type !== 'message' || event.message.type !== 'text') return;
  const text = (event.message.text || '').trim();
  const pid = matchProduct(text);
  if (!pid) {
    const reply: Message[] = [{ type:'text',
      text:'請傳「產品8/9/10/11」或關鍵字（Serum / Cleanse / Toner / Crème）。'}];
    await client.replyMessage((event as any).replyToken, reply);
    return;
  }
  await client.replyMessage((event as any).replyToken, [
    flexForProduct(pid) as any,
    { type:'text', text:`你選擇的是：${PRODUCT_NAME[pid]}` }
  ]);
}
function matchProduct(input: string): ProductId | undefined {
  const q = input.toLowerCase();
  for (const [k, aliases] of Object.entries(PRODUCT_ALIASES)) {
    const pid = Number(k) as ProductId;
    if (aliases.some(a => q === a.toLowerCase() || q.includes(a.toLowerCase()))) return pid;
  }
  return undefined;
}
const PORT = Number(process.env.PORT || 3000);
app.listen(PORT, () => console.log(`Listening on :${PORT}`));
