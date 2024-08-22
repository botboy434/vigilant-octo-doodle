import asyncio, datetime, json
from pytale import Py_Tale
import speech_recognition as sr
import threading
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import Qt
from qasync import QEventLoop
import signal

global running
running = False
r = sr.Recognizer()
server_id = 1906072840
phrase_lookup = {
    "short metal pointed handle": "HandleShortPointyEnd",
    "large green leather roll": "SoftFabricLargeRoll wyrmfaceleather",
    "large grey leather roll": "SoftFabricLargeRoll unknownleather",
    "large red leather roll": "SoftFabricLargeRoll daisleather",
    "brown mushroom shield": "BrownMushroomShield",
    "red wood arrow shaft": "ArrowShaftWooden Redwood",
    "teleportation potion": "PotionMedium",
    "medium fancy handle": "HandleMediumCurved",
    "medium metal handle": "HandleMediumCool",
    "red mushroom shield": "RedMushroomShield",
    "redwood arrow shaft": "ArrowShaftWooden Redwood",
    "green leather roll": "SoftFabricMediumRoll wyrmfaceleather",
    "large leather roll": "SoftFabricLargeRoll ",
    "large metal shield": "Shield",
    "short fancy handle": "HandleShortCool",
    "short metal handle": "HandleShortCCurve",
    "small metal shield": "SmallShield",
    "waka zasshi handle": "HebiosHandleWakizashi",
    "walnut arrow shaft": "ArrowShaftWooden Walnut",
    "why kizashi handle": "HebiosHandleWakizashi",
    "birch arrow shaft": "ArrowShaftWooden Birch",
    "grey leather roll": "SoftFabricMediumRoll unknownleather",
    "long metal handle": "HandleLargeCool",
    "metal fist handle": "HandleFist",
    "un ripe blueberry": "BlueberryFullUnripe",
    "waka zasshi blade": "MetalHebiosWakizashiBlade",
    "leather backpack": "Bag",
    "red leather roll": "SoftFabricMediumRoll daisleather",
    "un ripe eggplant": "EggplantFullUnripe",
    "unripe blueberry": "BlueberryFullUnripe",
    "wakizashi handle": "HebiosHandleWakizashi",
    "ash arrow shaft": "ArrowShaftWooden Ash",
    "crystal pickaxe": "CrystalPickBlue",
    "naginata handle": "HebiosHandleNaginata",
    "palladium ingot": "CarsiIngot",
    "read iron ingot": "RedIronIngot",
    "un ripe pumpkin": "pumpkinpieceunripe",
    "unripe eggplant": "EggplantFullUnripe",
    "wakizashi blade": "MetalHebiosWakizashiBlade",
    "woodcutting bag": "TimberBag",
    "electrum ingot": "WhiteGoldIngot",
    "hibiya scarred": "HebiosGuard",
    "naginata blade": "MetalHebiosNaginataBlade",
    "red iron ingot": "RedIronIngot",
    "spriggull meat": "SpriggullDrumstickFullCooked",
    "un ripe carrot": "CarrotFullUnripe",
    "un ripe garlic": "GarlicFullUnripe",
    "un ripe potato": "PotatoFullUnripe",
    "un ripe tomato": "TomatoFullUnripe",
    "unripe pumpkin": "pumpkinpieceunripe",
    "veridium ingot": "OrchiIngot",
    "viridium ingot": "OrchiIngot",
    "bellion ingot": "EvinonSteelIngot",
    "crystal lance": "CrystalLanceBlue",
    "crystal spike": "CrystalShardBlue",
    "crystal sword": "CrystalSwordBlue",
    "fabric square": "ThinClothMediumSquare",
    "hebrews arrow": "KaKarimataArrow",
    "hebrews guard": "HebiosGuard",
    "katana handle": "HebiosHandleKatana",
    "metal buckles": "HardMetalSmallBits",
    "mithril ingot": "MythrilIngot",
    "mythril ingot": "MythrilIngot",
    "phantom guard": "PhantomGuard",
    "spicy avocado": "ExplosiveSpike",
    "spriggle meat": "SpriggullDrumstickFullCooked",
    "turabada eyes": "ExplosiveSpike",
    "un ripe apple": "AppleFullUnripe",
    "un ripe onion": "OnionFullUnripe",
    "unripe carrot": "CarrotFullUnripe",
    "unripe garlic": "GarlicFullUnripe",
    "unripe potato": "PotatoFullUnripe",
    "unripe tomato": "TomatoFullUnripe",
    "Valiant ingot": "EvinonSteelIngot",
    "waikato sashi": "Wakizashi",
    "blue feather": "SpriggullFeatherBlue",
    "copper ingot": "CopperIngot",
    "foraging bag": "ForageBasketBag",
    "hebios arrow": "KaKarimataArrow",
    "hebios guard": "HebiosGuard",
    "hibiya farro": "KaKarimataArrow",
    "katana blade": "MetalHebiosKatanaBlade",
    "kunai handle": "HebiosHandleKunai",
    "leather roll": "SoftFabricMediumRoll ",
    "red wood bow": "Bow Redwood",
    "silver ingot": "SilverIngot",
    "tibios guard": "HebiosGuard",
    "unripe apple": "AppleFullUnripe",
    "unripe onion": "OnionFullUnripe",
    "valyan ingot": "EvinonSteelIngot",
    "wooden ladle": "WoodenLadle",
    "wooden stake": "WoodenStake",
    "wooden sword": "WoodenShortSword",
    "arrow shaft": "ArrowShaftWooden",
    "baboon meet": "BabuLegFullCooked",
    "crystal gem": "CrystalGemBlue",
    "healing pod": "HealingPod",
    "hebrews god": "HebiosGuard",
    "hoarder bag": "HoarderBag",
    "metal plate": "HardPlateMetalMediumSquare",
    "red feather": "SpriggullFeatherRed",
    "redwood bow": "Bow Redwood",
    "walnut wood": "woodcutwedge walnut",
    "wooden bowl": "WoodenBowl",
    "wooden club": "LargeSpikedWoodenClub",
    "wooden dice": "WoodenDice",
    "birch wood": "woodcutwedge birch",
    "candy cane": "CandyCane",
    "flashlight": "FlashlightLantern",
    "gold ingot": "GoldIngot",
    "iron ingot": "IronIngot",
    "mining bag": "OreBag",
    "potion bag": "BarrelBag",
    "sand stone": "SandstoneStone",
    "wakas ashi": "Wakizashi",
    "walnut bow": "Bow Walnut",
    "wooden net": "WoodenNet",
    "babu meat": "BabuLegFullCooked",
    "babu meet": "BabuLegFullCooked",
    "birch bow": "Bow Birch",
    "birchwood": "woodcutwedge birch",
    "fuel core": "MRKFuelCore",
    "gold coin": "GoldCoin",
    "metal bow": "MetalBow",
    "sai blade": "MetalHebiosSaiBlade",
    "sandstone": "SandstoneStone",
    "spy glass": "SpyGlass",
    "wakizashi": "Wakizashi",
    "ash wood": "woodcutwedge ash",
    "cauldron": "CauldronMedium",
    "dai meat": "DaisMeatFullCooked",
    "die meat": "DaisMeatFullCooked",
    "die meet": "DaisMeatFullCooked",
    "dye meat": "DaisMeatFullCooked",
    "dye meet": "DaisMeatFullCooked",
    "dynamite": "Dynamite",
    "firework": "Firework",
    "naginata": "Naginata",
    "oak wood": "woodcutwedge",
    "psyblade": "MetalHebiosSaiBlade",
    "red wood": "woodcutwedge redwood",
    "spyglass": "SpyGlass",
    "ash bow": "Bow Ash",
    "ashwood": "woodcutwedge ash",
    "lantern": "Lantern",
    "oakwood": "woodcutwedge",
    "redwood": "woodcutwedge redwood",
    "bucket": "WoodenBucket",
    "katana": "Katana",
    "quiver": "Quiver",
    "flint": "Flint",
    "geode": "GeodeTier1",
    "gored": "GourdCanteen",
    "gourd": "GourdCanteen",
    "grass": "GrassClump",
    "kunai": "KeyStandard",
    "stick": "Stick",
    "stone": "Stone",
    "coal": "Coal",
    "rope": "RopeClump",
    "salt": "Salt",
    "bow": "Bow Oak",
    "key": "KeyStandard",
    "psy": "Sai",
    "sai": "Sai",
}
phrases=('oakwood', 'birchwood', 'ashwood', 'redwood', 'psyblade', 'waka zasshi blade', 'hibiya farro', 'hebrews arrow', 'psy', 'wakas ashi', 'waikato sashi' 'spyglass', 'sand stone', 'read iron ingot', 'veridium ingot', 'mithril ingot', 'Valiant ingot', 'bellion ingot', 'red wood bow', 'red wood arrow shaft', 'gored', 'un ripe tomato', 'un ripe pumpkin', 'un ripe potato', 'un ripe onion', 'un ripe garlic', 'un ripe eggplant', 'un ripe carrot', 'spriggle meat', 'un ripe blueberry', 'un ripe apple', 'hebios guard',  'babu meet', 'dye meat', 'baboon meet', 'die meat', 'die meet', 'dye meet', 'waka zasshi handle', 'why kizashi handle', 'hibiya scarred', 'tibios guard', 'hebrews god', 'hebrews guard', 'oak wood', 'birch wood', 'walnut wood', 'ash wood', 'red wood', 'candy cane', 'katana blade', 'naginata blade', 'sai blade', 'wakizashi blade', 'hebios arrow', 'katana', 'kunai', 'naginata', 'sai', 'wakizashi', 'brown mushroom shield', 'red mushroom shield', 'wooden dice', 'spy glass', 'fuel core', 'stick', 'stone', 'sandstone', 'salt', 'grass', 'flint', 'crystal gem', 'coal', 'lantern', 'woodcutting bag', 'mining bag', 'hoarder bag', 'foraging bag', 'potion bag', 'leather backpack', 'electrum ingot', 'silver ingot', 'red iron ingot', 'viridium ingot', 'mythril ingot', 'iron ingot', 'gold ingot', 'valyan ingot', 'copper ingot', 'palladium ingot', 'gold coin', 'flashlight', 'firework', 'dynamite', 'small metal shield', 'large metal shield', 'quiver', 'metal bow', 'crystal sword', 'crystal pickaxe', 'crystal lance', 'bow', 'birch bow', 'walnut bow', 'ash bow', 'redwood bow', 'arrow shaft', 'birch arrow shaft', 'walnut arrow shaft', 'ash arrow shaft', 'redwood arrow shaft', 'teleportation potion', 'wooden stake', 'wooden net', 'geode', 'key', 'gourd', 'unripe tomato', 'unripe pumpkin', 'unripe potato', 'unripe onion', 'unripe garlic', 'unripe eggplant', 'unripe carrot', 'babu meat', 'dai meat', 'spriggull meat', 'unripe blueberry', 'unripe apple', 'red feather', 'blue feather', 'wakizashi handle', 'naginata handle', 'kunai handle', 'katana handle', 'metal fist handle', 'short metal pointed handle', 'short fancy handle', 'short metal handle', 'medium fancy handle', 'medium metal handle', 'long metal handle', 'fabric square', 'leather roll', 'red leather roll', 'grey leather roll', 'green leather roll', 'large leather roll', 'large red leather roll', 'large grey leather roll', 'large green leather roll', 'rope', 'metal plate', 'metal buckles', 'wooden sword', 'healing pod', 'turabada eyes', 'crystal spike', 'wooden club', 'phantom guard', 'wooden ladle', 'bucket', 'wooden bowl', 'cauldron')


async def command(command_to_run: str):
    """Send a manual command to the server, and replies with the response"""
    await bot.wait_for_ws()
    await bot.send_command_console(server_id, command_to_run)

async def startserver():
    """Starts a websocket console for the server"""
    await bot.wait_for_ws()
    await bot.create_console(server_id)

async def start():
    """Start voice recognition"""
    if not running:
        asyncio.create_task(voice_recog())

async def stop():
    """Stop voice recognition"""
    global stop_recognition
    stop_recognition = True

async def send_to_console(var1, var2):
    string = phrase_lookup.get(var1)
    num = int(var2)
    await bot.send_command_console(server_id, f'spawn botboy434 {string} {num}')
    print(f'spawn botboy434 {string} {num}')

async def start_voice_recognition():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    await loop.run_until_complete(await voice_recog())

async def voice_recog():
    global running
    global stop_recognition
    running = True
    stop_recognition = False

    while running:
        try:

            text = await asyncio.get_running_loop().run_in_executor(None, recognize_speech)
            text = text.lower()

            if "summon" in text or "salmon" in text:
                found_multi_word_phrase = None
                for phrase, action in phrase_lookup.items():
                    if phrase in text:
                        found_multi_word_phrase = phrase
                        break

                found_single_word_phrase = None
                words = text.split()
                for word in words:
                    if word in phrases:
                        found_single_word_phrase = word
                        break

                number = None
                for i, word in enumerate(words):
                    if word.isdigit():
                        number = int(word)
                        break

                if found_multi_word_phrase:
                    if number is None:
                        number = 1
                    await send_to_console(found_multi_word_phrase, number)
                elif found_single_word_phrase:
                    if number is None:
                        number = 1
                    await send_to_console(found_single_word_phrase, number)
            else:
                print("'Summon' or 'Salmon' was not found in the recognized text.")
                print(text)

            if stop_recognition:
                running = False
                print("Stopping voice recognition...")
                break

        except sr.UnknownValueError:
            print("Vosk Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Vosk Speech Recognition service; {e}")

def recognize_speech():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        r.dynamic_energy_threshold = True
        print("Say something!")
        audio = r.listen(source)
    text = r.recognize_vosk(audio)
    return text

async def on_ready():
    print("ready")
    asyncio.create_task(bot.run())
    await bot.wait_for_ws()
    await bot.create_console(server_id, timeout=5)

bot = Py_Tale()
bot.config(client_id='client_75e6b625-24c6-4021-880c-ad28cf4413f3',
           user_id=1971323560,
           scope_string='ws.group ws.group_members ws.group_servers ws.group_bans ws.group_invites group.info group.join group.leave group.view group.members group.invite server.view server.console',
           client_secret='',
           debug=True)

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bot Control GUI")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Command:")
        layout.addWidget(self.label)

        self.command_input = QLineEdit()
        layout.addWidget(self.command_input)

        self.start_button = QPushButton("Start Voice Recognition")
        self.start_button.clicked.connect(self.start_voice_recog)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Voice Recognition")
        self.stop_button.clicked.connect(self.stop_voice_recognition)
        layout.addWidget(self.stop_button)

        self.startserver_button = QPushButton("Start Server")
        self.startserver_button.clicked.connect(self.start_server)
        layout.addWidget(self.startserver_button)

        self.command_button = QPushButton("Send Command")
        self.command_button.clicked.connect(self.send_command)
        layout.addWidget(self.command_button)

        self.setLayout(layout)

    def start_voice_recog(self):
        asyncio.create_task(self._start_voice_recog())

    async def _start_voice_recog(self):
        await start()

    def stop_voice_recognition(self):
        asyncio.create_task(self._stop_voice_recognition())

    async def _stop_voice_recognition(self):
        await stop()

    def start_server(self):
        asyncio.create_task(self._start_server())

    async def _start_server(self):
        await startserver()

    def send_command(self):
        command_text = self.command_input.text()
        asyncio.create_task(self._send_command(command_text))

    async def _send_command(self, command_text):
        await command(command_text)


stop_event = asyncio.Event()

async def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show() 
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    def signal_handler(sig, frame):
        print("SIGINT received, stopping...")
        stop_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    with loop:
        try:
            await stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            app.quit()

if __name__ == '__main__':
    asyncio.run(main())