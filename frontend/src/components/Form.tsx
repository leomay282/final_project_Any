import { Field, Fieldset, Input, Label, Legend, Select } from '@headlessui/react';
import { ChevronDownIcon } from '@heroicons/react/16/solid';
import clsx from 'clsx';
import { ReactNode, useState } from 'react';
import yellowTaxi from '../images/yellow-taxi.png';
import { TaxiZone } from '../taxi-zones';
import ButtonComponent from './Button';
export interface FormValue {
  isFreeTrip: boolean;
  pickUpId: number;
  dropOffId: number;
  pickUpDateTime: string;
  passengersNumber: number;
  paymentMethodId: number;
}

const paymentMethods = [
  {
    label: 'Credit card',
    value: 1,
  },
  {
    label: 'Cash',
    value: 2,
  },
];

const SelectComponent = (props: React.SelectHTMLAttributes<HTMLSelectElement>) => {
  return (
    <div className='relative'>
      <Select
        className={clsx(
          'mt-3 block w-full appearance-none rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white',
          'focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25'
        )}
        {...props}>
        {props.children}
      </Select>
      <ChevronDownIcon className='group pointer-events-none absolute top-2.5 right-2.5 size-4 fill-white/60' aria-hidden='true' />
    </div>
  );
};

const LabelComponent = ({ children }: { children: ReactNode }) => {
  return <Label className='text-sm/6 font-medium text-white'> {children}</Label>;
};

const InputComponent = (props: React.InputHTMLAttributes<HTMLInputElement>) => {
  return (
    <Input
      className={clsx(
        'mt-3 block w-full rounded-lg border-none bg-white/5 py-1.5 px-3 text-sm/6 text-white',
        'focus:outline-none data-[focus]:outline-2 data-[focus]:-outline-offset-2 data-[focus]:outline-white/25'
      )}
      {...props}
    />
  );
};

const Form = ({ onSend, isLoading, zones }: { onSend: (formValue: FormValue) => void; isLoading: boolean; zones: TaxiZone[] }) => {
  const [pickUpId, setPickUpId] = useState(zones[0].LocationID.toString());
  const [dropOffId, setDropOffId] = useState(zones[1].LocationID.toString());
  const [pickUpDateTime, setPickUpDateTime] = useState('2024-06-19 15:54:00');
  const [passengersNumber, setPassengersNumber] = useState('1');
  const [paymentMethodId, setPaymentMethodId] = useState('1');

  return (
    <Fieldset className='space-y-6 '>
      <Legend className='text-base/7 font-semibold text-white text-center'>Plan your ride</Legend>
      <img src={yellowTaxi} alt='logo' className='w-auto h-20 mx-auto' />
      <Field>
        <LabelComponent>Pick up time</LabelComponent>
        <InputComponent
          type='datetime-local'
          value={pickUpDateTime}
          onChange={({ target }) => {
            setPickUpDateTime(target.value);
          }}
        />
      </Field>

      <Field>
        <LabelComponent>Pick up location</LabelComponent>
        <SelectComponent
          value={pickUpId}
          onChange={({ target }) => {
            setPickUpId(target.value);
          }}>
          {zones.map((zone) => (
            <option key={zone.LocationID} value={zone.LocationID}>
              {zone.Zone}
            </option>
          ))}
        </SelectComponent>
      </Field>

      <Field>
        <LabelComponent>Drop off location</LabelComponent>
        <SelectComponent
          value={dropOffId}
          onChange={({ target }) => {
            setDropOffId(target.value);
          }}>
          {zones.map((zone) => (
            <option key={zone.LocationID} value={zone.LocationID}>
              {zone.Zone}
            </option>
          ))}
        </SelectComponent>
      </Field>

      <Field>
        <LabelComponent>Passengers number</LabelComponent>

        <SelectComponent
          value={passengersNumber}
          onChange={({ target }) => {
            setPassengersNumber(target.value);
          }}>
          <option value={1}>1</option>
          <option value={2}>2</option>
          <option value={3}>3</option>
          <option value={4}>4</option>
          <option value={5}>5</option>
          <option value={6}>6</option>
          <option value={7}>7</option>
        </SelectComponent>
      </Field>

      <Field>
        <LabelComponent>Payment method</LabelComponent>
        <SelectComponent
          value={paymentMethodId}
          onChange={({ target }) => {
            setPaymentMethodId(target.value);
          }}>
          {paymentMethods.map((method) => (
            <option key={method.value} value={method.value}>
              {method.label}
            </option>
          ))}
        </SelectComponent>
      </Field>

      <div className='flex justify-end'>
        <ButtonComponent
          onClick={() => {
            onSend({
              isFreeTrip: false,
              pickUpDateTime,
              pickUpId: Number(pickUpId),
              dropOffId: Number(dropOffId),
              paymentMethodId: Number(paymentMethodId),
              passengersNumber: Number(paymentMethodId),
            });
          }}
          isLoading={isLoading}>
          Continue
        </ButtonComponent>
      </div>
    </Fieldset>
  );
};

export default Form;
