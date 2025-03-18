require('dotenv').config();
const fs = require('fs').promises;

const { Client, Events, GatewayIntentBits } = require('discord.js');

const client = new Client({ intents: [
  GatewayIntentBits.Guilds,
  GatewayIntentBits.GuildMessages,
  GatewayIntentBits.MessageContent
] });

const TOKEN = process.env.BOT_TOKEN

client.on(Events.ClientReady, readyClient => {
  console.log(`Logged in as ${readyClient.user.tag}!`);
});

client.on(Events.InteractionCreate, async (interaction) => {
    if (!interaction.isChatInputCommand()) return;

    if (interaction.commandName === 'dataset') {
        interaction.reply(`Saving messages...`);

        let lastMessageId = null;

        while(true){
            const options = { limit: 100 };
            if (lastMessageId) {
                options.before = lastMessageId;
            }

            const messages = await interaction.channel.messages.fetch(options);
            if (messages.size === 0) break;

            lastMessageId = messages.last().id;
            
            await fs.appendFile(
                'dataset.txt', 
                [...messages.values()].map(msg => `${msg.author.tag}: ${msg.content}`).join("\n")
            )
        }
    }
});
    
client.login(TOKEN);