import logging

from sqlalchemy.ext.asyncio import AsyncSession
from data.models import Patient

from sqlalchemy import select

from typing import Optional, List

from utils.logger_settings import setup_logging

logger = logging.getLogger(setup_logging())


async def add_patient(session: AsyncSession,
                      user_id: int,
                      user_name: str,
                      phone: str, ) -> Optional[Patient]:
    patient = await session.scalar(select(Patient).where(Patient.user_id == user_id))
    try:
        if not patient:
            session.add(Patient(
                user_name=user_name,
                user_id=user_id,
                phone=phone,
            )
            )
            await session.commit()
            logger.info("Пациент %s добавлен", user_id)
            return patient
        else:
            logger.info("Пациент %s найден", user_id)
    except Exception as ex:
        logger.error("Ошибка при добавлении пациента %e", ex)


async def select_all_patient(session: AsyncSession) -> Optional[List[Patient]]:
    patients = await session.scalars(select(Patient))
    logger.info("Все пациенты")
    return patients.all()


async def patient_filter(session: AsyncSession, **kwargs) -> Optional[List[Patient]]:
    patients = await session.scalars(select(Patient).where(**kwargs))
    return patients.all()


async def delete_patient(session: AsyncSession, **kwargs):
    patient = await session.scalar(select(Patient).where(**kwargs))
    if patient:
        await session.delete(patient)
        await session.commit()
        logger.info("Пациент %s удален", patient.user_id)
    else:
        logger.info("Пациент %s не найден", kwargs.get("user_id"))


async def update_patient(session: AsyncSession, user_id: int, **kwargs) -> Optional[Patient]:
    patient = await session.scalar(select(Patient).where(Patient.user_id == user_id))
    if patient:
        for key, value in kwargs.items():
            setattr(patient, key, value)
        await session.commit()
        logger.info("Пациент %s обновлен", user_id)
        return patient
    else:
        logger.info("Пациент %s не найден", user_id)
        return None


async def get_patient(session: AsyncSession, **kwargs) -> Optional[Patient]:
    # Создаем базовый запрос
    query = select(Patient)

    # Добавляем условия фильтрации
    for key, value in kwargs.items():
        query = query.where(getattr(Patient, key) == value)

    # Выполняем запрос
    patient = await session.scalar(query)

    if not patient:
        logger.info("Пациент %s не найден", kwargs.get("user_id"))

    return patient
