# pip install -U pytest
# צריך שקובץ בדיקה תתחיל במילה טסט_ או תסיים במילה _טסט
# צריך שפונקציית הבדיקה תתחיל בטסט_ בקלאס להתחיל בטסט
# להפריד בין קובץ פונקציות לבדיקות
# הרצה הבדיקות עם פקודה  pytest בטרמניל
# לכתוב לכל פונקציה את שם הבדיקה בצורה
# לבדוק 3 בדיקות שעובורות, כל בדיקות חריגות, בדיקה של פרמטרים
from services.caloulter_actions import calculator_atr


def test_atr_cal():
    assert isinstance(calculator_atr(3.5, 60), float)
    assert calculator_atr(30, 10) == 3
    assert calculator_atr(100, 50) == 2
    assert calculator_atr('100', 100)