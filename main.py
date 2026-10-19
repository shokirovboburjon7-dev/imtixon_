import asyncio
import logging
from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = "8956899696:AAHFHgTlIlVXTS4qPaG7xgslliiexPofYS0"

router = Router()

class RegistrationState(StatesGroup):
    full_name = State()
    phone = State()
    choose_course = State()
    confirm = State()

COURSES = {
    "python": {"name": "Python", "duration": "5 oy", "price": "1,200,000 so'm/oy"},
    "web": {"name": "Web dasturlash", "duration": "7 oy", "price": "1,500,000 so'm/oy"},
    "frontend": {"name": "Frontend", "duration": "4 oy", "price": "1,300,000 so'm/oy"},
    "graphic": {"name": "Grafik dizayn", "duration": "3 oy", "price": "1,000,000 so'm/oy"}
}

def get_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 Kurslar"), KeyboardButton(text="📝 Kursga yozilish")],
            [KeyboardButton(text="ℹ️ Markaz haqida"), KeyboardButton(text="📞 Aloqa")]
        ],
        resize_keyboard=True
    )

def get_cancel_menu():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! O'quv markazimizning rasmiy botiga xush kelibsiz. Kerakli bo'limni tanlang:",
        reply_markup=get_main_menu()
    )

@router.message(F.text == "📚 Kurslar")
async def show_courses(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Python", callback_data="course_python")],
            [InlineKeyboardButton(text="Web dasturlash", callback_data="course_web")],
            [InlineKeyboardButton(text="Frontend", callback_data="course_frontend")],
            [InlineKeyboardButton(text="Grafik dizayn", callback_data="course_graphic")]
        ]
    )
    await message.answer("Bizning o'quv markazimizda mavjud kurslar:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("course_"))
async def course_detail(callback: CallbackQuery):
    course_key = callback.data.split("_")[1]
    course = COURSES.get(course_key)
    if course:
        text = (
            f"<b>Kurs nomi:</b> {course['name']}\n"
            f"<b>Davomiyligi:</b> {course['duration']}\n"
            f"<b>Narxi:</b> {course['price']}"
        )
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@router.message(F.text == "ℹ️ Markaz haqida")
async def about_center(message: Message):
    await message.answer("🏢 Bizning o'quv markazimiz zamonaviy kasblarni o'rgatadi.")

@router.message(F.text == "📞 Aloqa")
async def contact_us(message: Message):
    await message.answer("📞 Telefon: +998 90 123-45-67\nTelegram: @oq_markaz_admin")

@router.message(F.text == "❌ Bekor qilish")
async def cancel_process(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Jarayon bekor qilindi.", reply_markup=get_main_menu())

@router.message(F.text == "📝 Kursga yozilish")
async def start_registration(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.full_name)
    await message.answer("Ism va familiyangizni kiriting:", reply_markup=get_cancel_menu())

@router.message(RegistrationState.full_name)
async def process_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await state.set_state(RegistrationState.phone)
    await message.answer("Telefon raqamingizni kiriting:")